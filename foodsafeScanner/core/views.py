from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
from .forms import SignUpForm,PreferencesForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import Preferences



def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username,password=password)
            login(request,user)
            return redirect('preferences')
    else:
        form = SignUpForm()
        return render(request,'signup.html',{
            'form':form
            })
    return render(request,'signup.html',{
            'form':form
            })

@login_required
def preferences(request):
    if request.method == 'POST':
        form = PreferencesForm(request.POST)
        if form.is_valid():
            preferences = form.save(commit=False)
            preferences.user = request.user
            preferences.save()
            return redirect('home')
    else:
        form = PreferencesForm()
    return render(request,'preferences.html',{'form':form})

@login_required
def home(request):
    return render(request, 'home.html')

def index(request):
    return render(request,'index.html')

@login_required
def scan_barcode(request):
    if request.method == 'POST':
        barcode_data = request.GET.get('barcode')
        print(barcode_data)
        # Process the barcode data (e.g., save it to the database)
        # return JsonResponse({'message': 'Barcode scanned successfully', 'barcode': barcode_data})
        return render('product.html',{'barcode':barcode_data})
    else:
        return JsonResponse({'message': 'Invalid request method'})


@csrf_exempt
def process_barcode(request):
    if request.method == 'POST':
        barcode_number = request.POST.get('barcode')
        # Process the barcode number (e.g., save it to the database)
        return JsonResponse({'status': 'success', 'barcode': barcode_number})
        return render('product.html',{'barcode':barcode_number})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})




def product_page(request):
    barcode = request.GET.get('barcode','')
    url=f'https://world.openfoodfacts.org/api/v2/product/{barcode}?fields=code,abbreviated_product_name,brands,additives_n,additives_original_tags,additives_tags,allergens,allergens_from_ingredients,allergens_hierarchy,allergens_tags,categories_hierarchy,categories_tags,warnings,ecoscore_grade,ecoscore_extended_data_version,image_url,ingredients,ingredients_analysis,ingredients_analysis_tags,ingredients_hierarchy,ingredients_tags,ingredients_text,ingredients_text_with_allergens,ingredients_text_with_allergens_en,labels_hierarchy,labels_tags,nova_group,nova_groups_markers,nova_groups_tags,nutrient_levels,nutrient_levels_tags,nutriments,nutriscore_grade,product_name,quantity,status,unknown_nutrients_tags,status_verbose'
    
    headers={
        "User-Agent": "FoodSafe/1.0 (shivforcollege@gmail.com)"
    }
    response=requests.get(url,headers=headers).json()

    if (response['status']):
        user_preference = Preferences.objects.get(user=request.user)

        # logic for user preference matching

        # adding all preferences weight set by user
        total_weight = user_preference.nutri_score_weight+user_preference.vegan_weight+user_preference.vegetarian_weight+user_preference.palm_oil_free_weight+user_preference.eco_score_weight+user_preference.gluten_weight+user_preference.milk_weight+user_preference.nuts_weight+user_preference.peanuts_weight+user_preference.soybeans_weight+user_preference.additives_weight+user_preference.nova_group_weight

        # total weight of nutri eco nova

        total_nutri_eco_nova_weight=user_preference.nutri_score_weight+user_preference.eco_score_weight+user_preference.nova_group_weight



        weighted_sum=0


        # extracting data from api
        product_data = response.get("product")
        # nutriscore
        nutri_score_values = {"a": 1, "b": 0.8, "c": 0.6, "d": 0.4, "e": 0.2}
        nutri_score = nutri_score_values.get(product_data.get('nutriscore_grade','').lower(), 0)
        print(nutri_score)
        # vegan
        vegan = 1 if 'en:vegan' in product_data.get('ingredients_analysis_tags', []) else 0
        print(vegan)
        non_vegan_ingredients= []
        if (vegan != 1):
            non_vegan_ingredients = response.get('product',{}).get('ingredients_analysis',{}).get('en:non-vegan',[])

        # vegetarian
        vegetarian = 1 if 'en:vegetarian' in product_data.get('ingredients_analysis_tags', []) else 0
        print(vegetarian)
        non_vegetarian_ingredients =[]
        if (vegetarian != 1):
            non_vegetarian_ingredients = response.get('product', {}).get('ingredients_analysis', {}).get('en:non-vegetarian', [])
            


        # palm_oil_free
        palm_oil_free = 1 if 'en:palm-oil-free' in product_data.get('ingredients_analysis_tags', []) else 0
        print(palm_oil_free)
        palm_oil_ingredients = []
        if (palm_oil_free != 1):
            palm_oil_ingredients = response.get('product', {}).get('ingredients_analysis', {}).get('en:palm-oil', [])
        

        # eco_score
        eco_score_values = {"a": 100, "b": 80, "c": 60, "d": 40, "e": 20}
        eco_score = eco_score_values.get(product_data.get('ecoscore_grade','').lower(),0)
        print(eco_score)
        # gluten free
        gluten_free = 1 if 'en:no-gluten' in product_data.get('labels_hierarchy',[]) else 0
        print(gluten_free)
        # milk_free
        milk_free = 0 if 'en:milk' in product_data.get('allergens_tags', []) else 1
        print(milk_free)
        # nuts free
        nuts_free = 0 if 'en:nuts' in product_data.get('allergens_tags', []) else 1
        print(nuts_free)
        # peanuts free
        peanuts_free = 0 if 'en:peanuts' in product_data.get('allergens_tags', []) else 1
        print(peanuts_free)
        # soybeans free
        soybeans_free = 0 if 'en:soybeans' in product_data.get('allergens_tags', []) else 1
        print(soybeans_free)
        # additives
        # if additives info is not given we are taking a additives count as 5
        additives_count = product_data.get('additives_n',5)
        print(additives_count)

        # nova group
        nova_group = product_data.get('nova_group', 4)
        print(nova_group)

        # adding all weighted sum
        weighted_sum += user_preference.nutri_score_weight * (nutri_score)
        weighted_sum += user_preference.vegan_weight * vegan
        weighted_sum += user_preference.vegetarian_weight * vegetarian
        weighted_sum += user_preference.palm_oil_free_weight * palm_oil_free
        weighted_sum += user_preference.eco_score_weight * (eco_score / 100)
        weighted_sum += user_preference.gluten_weight * gluten_free
        weighted_sum += user_preference.milk_weight * milk_free
        weighted_sum += user_preference.nuts_weight * nuts_free
        weighted_sum += user_preference.peanuts_weight * peanuts_free
        weighted_sum += user_preference.soybeans_weight * soybeans_free
        weighted_sum += user_preference.additives_weight * (1 - additives_count / 10)  # Invert additives count: lower is better
        weighted_sum += user_preference.nova_group_weight* (1 - nova_group / 4)
        # calculating percentage of user pereferences match with product
        
        if(total_weight<=0 and total_nutri_eco_nova_weight<=0):
            #if user has set all thing as not important then every product will met their requirements
            percentage_match = 100.00
            percentage_match_nutri_nova_eco=100.00

            return render(request,'scan_result.html',{'response':response,'percentage_match':percentage_match,'palm_oil_free':palm_oil_free,'vegan':vegan,'vegetarian':vegetarian,'palm_oil_ingredients':palm_oil_ingredients,'non_vegan_ingredients':non_vegan_ingredients,'non_vegetarian_ingredients':non_vegetarian_ingredients,'percentage_match_nutri_nova_eco':percentage_match_nutri_nova_eco})



        percentage_match = (weighted_sum / total_weight) * 100
        percentage_match = round(percentage_match,2)
        print(f"The product match user preferences by {percentage_match:.2f}%")


        # adding nutri eco nova weight
        nutri_eco_nova_weight = user_preference.nutri_score_weight * (nutri_score)+user_preference.eco_score_weight * (eco_score / 100)+user_preference.nova_group_weight* (1 - nova_group / 4)

        percentage_match_nutri_nova_eco = 0
        percentage_match_nutri_nova_eco = (nutri_eco_nova_weight/total_nutri_eco_nova_weight)*100
        percentage_match_nutri_nova_eco = round(percentage_match_nutri_nova_eco,2)
        print(percentage_match_nutri_nova_eco)
        
        return render(request,'scan_result.html',{'response':response,'percentage_match':percentage_match,'palm_oil_free':palm_oil_free,'vegan':vegan,'vegetarian':vegetarian,'palm_oil_ingredients':palm_oil_ingredients,'non_vegan_ingredients':non_vegan_ingredients,'non_vegetarian_ingredients':non_vegetarian_ingredients,'percentage_match_nutri_nova_eco':percentage_match_nutri_nova_eco})

    else:
        return render(request,'scan_result.html',{'response':response})




























# def search_product_by_barcode(request):
#     if request.method == 'POST':
#         try:
#             barcode = request.POST['barcode']
#             return JsonResponse({'success': True, 'data': barcode}, content_type='application/json')
#         except KeyError:
#             # Handle the case where 'barcode' key is not found in POST data
#             return JsonResponse({'success': False, 'error': 'Barcode not provided'}, content_type='application/json')
#     return JsonResponse({'success': False, 'error': 'Invalid request method'}, content_type='application/json')




# response_product = response.get("product")
    # response_product_category = response_product.get("categories_hierarchy")
    # print(response_product_category)
    # allergens = response_product.get("allergens")

    # alternative_products_url = f'https://world.openfoodfacts.org/api/v2/search?categories_tags_en={response_product_category[0]},{response_product_category[1]},{response_product_category[2]}&fields=product_name,code,allergens'
    # alternative_product_response = requests.get(alternative_products_url,headers=headers).json()