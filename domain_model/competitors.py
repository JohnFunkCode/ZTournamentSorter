""" this module contains code to manage a collection of competitors """

import logging
import pandas as pd


class Competitors(pd.DataFrame):
    ''' class to manage a list of competitor'''

    @property
    def _constructor(self):
        return Competitors

    def __init__(self, data=None, index=None, columns=None, dtype=None, copy=False):
        '''setup instance variables'''
        super().__init__(data, index, columns, dtype, copy)

    def __repr__(self):
        '''return the string representation of the DataFrame'''
        return super().__repr__()

    def get_number_of_competitors(self) -> int:
        '''convenience  method to get the number of competitors'''
        return self.shape[0]

    def sort_by_body_mass_index_and_dojo(self):
        ''' sort the competitors by ascending BMI and Dojo'''
        return_df=self.sort_values(by=['BMI', 'Dojo'])
        return return_df

    def arrange_competitors_for_sparring(self):
        ''' arrange competitors by BMI and so ajacent competitors are from different dojos (if possible) '''
        result_list = []

        comps = self

        comps = comps.sort_by_body_mass_index_and_dojo()

        while comps.shape[0] > 1:
            name1 = comps.iloc[0]['First_Name']
            reg_id_1 = comps.iloc[0]['Registrant_ID']
            dojo1 = comps.iloc[0]['Dojo']
            name2 = ''
            reg_id_2 = ''

            # dojo2 = ''
            for i in range(1, len(comps)):
                # scan the list for a competitor from a different dojo
                if comps.iloc[i].Dojo != dojo1:
                    # logging.info(i,"Found a Different Dojo")
                    name2 = comps.iloc[i]['First_Name']
                    reg_id_2 = comps.iloc[i]['Registrant_ID']
                    dojo2 = comps.iloc[i]['Dojo']
                    break

            # if we fell out of the loop without find a competitor from a different dojo, just take the next competitor in the list
            if reg_id_2 == '':
                #logging.info("No Competitor from a different Dojo - we'll use the next person in the list")
                name2 = comps.iloc[1]['First_Name']
                reg_id_2 = comps.iloc[1]['Registrant_ID']
                dojo2 = comps.iloc[1]['Dojo']
                i=1  #don't forget to set the index back to the first competitor

            # add the two competitors to the result list
            result_list.append(comps.iloc[0])
            result_list.append(comps.iloc[i])

            # remove the two competitors names from main list
            df1 = comps[comps['Registrant_ID'] != reg_id_1]
            comps = df1[df1['Registrant_ID'] != reg_id_2]

        #  done with the while loop - if we still have someone in the list add them to the result list
        # if (comps.shape[0] % 2) != 0:
        if comps.shape[0] > 0:
            name1 = comps.iloc[0]['First_Name']
            reg_id_1 = comps.iloc[0]['Registrant_ID']
            dojo1 = comps.iloc[0]['Dojo']
            # logging.info(name1, dojo1)
            result_list.append(comps.iloc[0])

        # create a DataFrame object with the result_list
        # logging.info(result_list)
        column_names = comps.columns.values.tolist()
        # logging.info(column_names)
        # logging.info(result_list)
        result_df = Competitors(data=result_list, columns=column_names)
        return result_df


if __name__ == '__main__':
    '''test getting the number of Competitors '''
    cols = ['Registrant_ID', 'First_Name', 'Last_Name', 'Gender', 'Dojo', 'Age', 'Rank', 'Feet', 'Inches', 'Height',
            'Weight', 'BMI', 'Events', 'Weapons', 'hitcount']
    data = [(255, 'Lucas', 'May', 'Male', 'CO- Parker', 10, 'Yellow', 4, 3, '4 ft. 3 in.', 52, 154,
             '2 Events - Forms & Sparring ($75)', 'None', 0),
            (194, 'jake', 'coleson', 'Male', 'CO- Cheyenne Mountain', 10, 'Yellow', 4, 0, '4', 60, 156,
             '2 Events - Forms & Sparring ($75)', 'Weapons ($35)', 0),
            (195, 'katie', 'coleson', 'Female', 'CO- Cheyenne Mountain', 12, 'White', 4, 0, '4', 65.161,
             '2 Events - Forms & Sparring ($75)', 'Weapons ($35)', 0)]
    df = pd.DataFrame(data, columns=cols)
    #      c = competitors.Competitors(df)
    # c = Competitors()
    c = Competitors(data, columns=cols)
    s = c.get_number_of_competitors()
    logging.info(s)
