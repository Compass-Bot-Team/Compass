# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import itertools
import random

atlantic_list = (list(map(''.join, itertools.product(*((c.upper(), c.lower()) for c in 'Atl')))) + list(
    map(''.join, itertools.product(*((c.upper(), c.lower()) for c in 'Atlantic')))))
epac_list = (list(map(''.join, itertools.product(*((c.upper(), c.lower()) for c in 'Epac')))) + list(
    map(''.join, itertools.product(*((c.upper(), c.lower()) for c in 'Eastern Pacific')))) + list(
    map(''.join, itertools.product(*((c.upper(), c.lower()) for c in 'East Pacific')))))
cpac_list = (list(map(''.join, itertools.product(*((c.upper(), c.lower()) for c in 'Cpac')))) + list(
    map(''.join, itertools.product(*((c.upper(), c.lower()) for c in 'Central Pacific')))))

numbers = ['One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Eleven', 'Twelve', 'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen', 'Twenty', 'Twenty-One', 'Twenty-Two', 'Twenty-Three', 'Twenty-Four', 'Twenty-Five', 'Twenty-Six', 'Twenty-Seven', 'Twenty-Eight', 'Twenty-Nine', 'Thirty', 'Thirty-One', 'Thirty-Two', 'Thirty-Three', 'Thirty-Four', 'Thirty-Five', 'Thirty-Six', 'Thirty-Seven', 'Thirty-Eight', 'Thirty-Nine', 'Fourty', 'Fourty-One', 'Fourty-Two', 'Fourty-Three', 'Fourty-Four', 'Fourty-Five', 'Fourty-Six', 'Fourty-Seven', 'Fourty-Eight', 'Fourty-Nine', 'Fifty', 'Fifty-One', 'Fifty-Two', 'Fifty-Three', 'Fifty-Four', 'Fifty-Five']
_2026atlhurricanelist = ["Arthur", "Bertha", "Cristobal", "Dolly", "Edouard", "Fay", "Gonzalo", "Hanna", "Isaias", "Josephine", "Kyle", "Marco", "Nana", "Omar", "Paulette", "Rene", "Sally", "Teddy", "Vicky", "Wilfred"]
_2021atlhurricanelist = ["Ana", "Bill", "Claudette", "Danny", "Elsa", "Fred", "Grace", "Henri", "Ida", "Julian", "Kate", "Larry", "Mindy", "Nicholas", "Odette", "Peter", "Rose", "Sam", "Teresa", "Victor", "Wanda"]
_2022atlhurricanelist = ["Alex", "Bonnie", "Colin", "Danielle", "Earl", "Fiona", "Gaston", "Hermine", "Ian", "Julia", "Karl", "Lisa", "Martin", "Nicole", "Owen", "Paula", "Richard", "Shary", "Tobias", "Virginie", "Walter"]
_2023atlhurricanelist = ["Arlene", "Bret", "Cindy", "Don", "Emily", "Franklin", "Gert", "Harold", "Idalia", "Jose", "Katia", "Lee", "Margot", "Nigel", "Ophelia", "Philippe", "Rina", "Sean", "Tammy", "Vince", "Whitney"]
_2024atlhurricanelist = ["Alberto", "Beryl", "Chris", "Debby", "Ernesto", "Francine", "Gordon", "Helene", "Isaac", "Joyce", "Kirk", "Leslie", "Milton", "Nadine", "Oscar", "Patty", "Rafael", "Sara", "Tony", "Valerie", "William"]
_2025atlhurricanelist = ["Andrea", "Barry", "Chantal", "Erin", "Fernand", "Gabrielle", "Humberto", "Imelda", "Jerry", "Karen", "Lorenzo", "Melissa", "Nestor", "Olga", "Pablo", "Rebekah", "Sebastien", "Tanya", "Van", "Wendy"]
greekhurricanelist = ["Alpha", "Beta", "Gamma", "Delta", "Epsilon", "Zeta", "Eta", "Theta", "Iota", "Kappa", "Lambda", "Mu", "Nu", "Xi", "Omicron", "Pi", "Rho", "Sigma", "Tau", "Upsilon", "Phi", "Chi", "Psi", "Omega"]
_2021epachurricanelist = ["Andres", "Blanca", "Carlos", "Dolores", "Enrique", "Felicia", "Guillermo", "Hilda", "Ignacio", "Jimena", "Kevin", "Linda", "Marty", "Nora", "Olaf", "Pamela", "Rick", "Sandra", "Terry", "Vivian", "Waldo", "Xina", "York", "Zelda"]

async def acceptable(chance):
    if chance > 0:
        acceptable = [30, 35, 40, 45, 50]
    if chance > 20:
        acceptable = [35, 40, 45, 50, 60, 65]
    if chance > 30:
        acceptable = [40, 45, 50, 60, 65, 70]
    if chance > 50:
        acceptable = [45, 50, 60, 65, 70, 75]
    if chance > 60:
        acceptable = [50, 60, 65, 70, 75, 80, 85, 90, 100]
    if chance > 70:
        acceptable = [50, 60, 65, 70, 75, 80, 85, 90, 100, 105, 110, 115, 125, 130, 140]
    if chance > 80:
        acceptable = [60, 65, 70, 75, 80, 85, 90, 100, 105, 110, 115, 120, 125, 130, 140, 145, 150, 155, 160]
    if chance > 90:
        acceptable = [80, 85, 90, 100, 105, 110, 115, 120, 125, 130, 140,
                      145, 150, 155, 160, 165, 175, 180]
    if chance > 95:
        acceptable = [90, 100, 105, 110, 115, 120, 125, 130, 140,
                      145, 150, 155, 160, 165, 175, 180, 185, 190, 195]
    return acceptable

async def classify(mph, location):
    global classification
    if mph > 0:
        classification = "Tropical Depression"
    if mph > 39:
        if location != "Eastern Pacific":
            ts_or_ss = random.randint(0, 100)
            if ts_or_ss > 15 and location != "Eastern Pacific":
                classification = "Tropical Storm"
            else:
                classification = "Subtropical Storm"
        else:
            classification = "Tropical Storm"
    if mph > 74:
        classification = "Hurricane"
    if mph > 110:
        classification = "Major Hurricane"
    return classification

async def hurricane_list_calc(year, location):
    if year == 2021:
        if location is None:
            hurricane_list = (_2021atlhurricanelist + greekhurricanelist)
        elif location == "Atlantic":
            hurricane_list = (_2021atlhurricanelist + greekhurricanelist)
        elif location == "Eastern Pacific":
            hurricane_list = (_2021epachurricanelist + greekhurricanelist)
    elif year == 2022:
        hurricane_list = (_2022atlhurricanelist + greekhurricanelist)
    elif year == 2023:
        hurricane_list = (_2023atlhurricanelist + greekhurricanelist)
    elif year == 2024:
        hurricane_list = (_2024atlhurricanelist + greekhurricanelist)
    elif year == 2025:
        hurricane_list = (_2025atlhurricanelist + greekhurricanelist)
    elif year == 2026:
        hurricane_list = (_2026atlhurricanelist + greekhurricanelist)
    return hurricane_list

async def hurricane_amount_calc(la_nina_or_el_nino):
    if la_nina_or_el_nino == 'La Nina':
        hurricane_amount = random.randint(5, 36)
    elif la_nina_or_el_nino == 'El Nino':
        hurricane_amount = random.randint(2, 13)
    return hurricane_amount
