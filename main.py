import pandas as pd 
import requests
from bs4 import BeautifulSoup

def scrape_recipe(url):
  response=requests.get(url) 
  soup =BeautifulSoup(response.content, 'html.parser')

  title=soup.find('h1').get_text()
  ingredients = [item.get_text() for item in soup.find_all(class_='ingredient')]
  instructions = soup.find(class_='instructions').get_text() 
  return{
    'Title': title, 
    'Ingredients': ingredients, 
    'Instructions': instructions, 
  }

def save_recipe (recipe):
  try:
    data = pd.read_csv('recipe.csv')
  except FileNotFoundError:
   data= pd.DataFrame(columns=['Title','Ingredients', 'Instructions'])

  new_recipe= pd.DataFrame({
    'Title': [recipe['Title']],
    'Ingredients': [', '.join(recipe['Ingredients'])], 
    'Instructions': [recipe ['Instructions']]
  })

  data= pd.concat([data, new_recipe],ignore_index=True)
  data.to_csv('recipe.csv',index=False)

def load_recipe():
  try:
    data= pd.read_csv('recipe.csv')
    return data
  except FileNotFoundError:
    return pd.DataFrame(columns=['Title','Ingredients', 'Instructions'])
    
    def main():
    while True:
        print("\nRecipe Book")
        print("1. Add Recipe from URL")
        print("2. Search Recipes by Ingredient")
        print("3. View All Recipes")
        print("4. Exit")
        
        choice = input("Choose an option: ")
        
        if choice == '1':
            url = input("Enter recipe URL: ")
            recipe = scrape_recipe(url)
            save_recipe(recipe)
            print(f"Recipe '{recipe['Title']}' added.")
        elif choice == '2':
            ingredient = input("Enter ingredient to search for: ")
            recipes = load_recipes()
            filtered_recipes = recipes[recipes['Ingredients'].str.contains(ingredient, case=False, na=False)]
            print(filtered_recipes)
        elif choice == '3':
            recipes = load_recipes()
            print(recipes)
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
