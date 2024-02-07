import glob
import pandas as pd
import pprint

class OrderMenu():
    
    def __init__(self):
        recipe_list = glob.glob('recipes/*')
        self.recipes = dict()
        self.all_recipes = []
        self.all_orders = []

        for x in recipe_list:
            df = pd.read_csv(x, index_col=0)
            df['amt'] = df['amt'].round(2)
            df['ingredient'] = df['ingredient'].str.capitalize()
            #print()
            self.recipes[x[:-4].split('\\')[1]] = df
            self.all_recipes.append(x[:-4].split('\\')[1])
    
    def menu(self):
        pprint.pprint(f'Please enter the equivalent number from the following items,' \
                      +' then write `checkouts`; or enter `quit` to exit:')
        pprint.pprint(list(enumerate(self.all_recipes)))
        choice = ''
        while (choice != 'quit') and (choice != 'show me'):
            choice = input()
            if choice == 'quit':
                print('exiting')

            elif choice == 'checkout':
                return self.checkout()
            else:
                try:
                    self.add_item(self.all_recipes[int(choice)])
                    print(f'adding {self.all_recipes[int(choice)]} to the order list')

                except:
                    print(f'cant add {choice} to the orders')
    
    def add_items(self, item_list):
        self.all_orders += item_list

    
    def add_item(self, choice):
        self.all_orders += [choice]
    
    def checkout(self):
        df = self.recipes[self.all_orders[0]]
        for x in self.all_orders[1:]:
            df = pd.concat([df, self.recipes[x]], axis=0)
            # print(df)
   
        
        print(df.groupby(['ingredient', 'measure'])['amt'].sum().reset_index()[['amt','measure', 'ingredient']])
    
    
if __name__ == '__main__':
    OrderMenu().menu()