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
_2021atlhurricanelist = ["Ana", "Bill", "Claudette", "Danny", "Elsa", "Fred", "Grace", "Henri", "Ida", "Julian", "Kate", "Larry", "Mindy", "Nicholas", "Odette", "Peter", "Rose", "Sam", "Teresa", "Victor", "Wanda"]
_2022atlhurricanelist = ["Alex", "Bonnie", "Colin", "Danielle", "Earl", "Fiona", "Gaston", "Hermine", "Ian", "Julia", "Karl", "Lisa", "Martin", "Nicole", "Owen", "Paula", "Richard", "Shary", "Tobias", "Virginie", "Walter"]
_2023atlhurricanelist = ["Arlene", "Bret", "Cindy", "Don", "Emily", "Franklin", "Gert", "Harold", "Idalia", "Jose", "Katia", "Lee", "Margot", "Nigel", "Ophelia", "Philippe", "Rina", "Sean", "Tammy", "Vince", "Whitney"]
_2024atlhurricanelist = ["Alberto", "Beryl", "Chris", "Debby", "Ernesto", "Francine", "Gordon", "Helene", "Isaac", "Joyce", "Kirk", "Leslie", "Milton", "Nadine", "Oscar", "Patty", "Rafael", "Sara", "Tony", "Valerie", "William"]
_2025atlhurricanelist = ["Andrea", "Barry", "Chantal", "Dexter", "Erin", "Fernand", "Gabrielle", "Humberto", "Imelda", "Jerry", "Karen", "Lorenzo", "Melissa", "Nestor", "Olga", "Pablo", "Rebekah", "Sebastien", "Tanya", "Van", "Wendy"]
_2026atlhurricanelist = ["Arthur", "Bertha", "Cristobal", "Dolly", "Edouard", "Fay", "Gonzalo", "Hanna", "Isaias", "Josephine", "Kyle", "Leah", "Marco", "Nana", "Omar", "Paulette", "Rene", "Sally", "Teddy", "Vicky", "Wilfred"]
_2021epachurricanelist = ["Andres", "Blanca", "Carlos", "Dolores", "Enrique", "Felicia", "Guillermo", "Hilda", "Ignacio", "Jimena", "Kevin", "Linda", "Marty", "Nora", "Olaf", "Pamela", "Rick", "Sandra", "Terry", "Vivian", "Waldo", "Xina", "York", "Zelda"]
_2022epachurricanelist = ["Agatha", "Blas", "Celia", "Darby", "Estelle", "Frank", "Georgette", "Howard", "Ivette", "Javier", "Kay", "Lester", "Madeline", "Newton", "Orlene", "Paine", "Roslyn", "Seymour", "Tina", "Virgil", "Winifred", "Xavier", "Yolanda", "Zeke"]
_2023epachurricanelist = ["Adrian", "Beatriz", "Calvin", "Dora", "Eugene", "Fernanda", "Greg", "Hilary", "Irwin", "Jova", "Kenneth", "Lidia", "Max", "Norma", "Otis", "Pilar", "Ramon", "Selma", "Todd", "Veronica", "Wiley", "Xina", "York", "Zelda"]
_2024epachurricanelist = ["Aletta", "Bud", "Carlotta", "Daniel", "Emilia", "Fabio", "Gilma", "Hector", "Ileana", "John", "Kristy", "Lane", "Miriam", "Norman", "Olivia", "Paul", "Rosa", "Sergio", "Tara", "Vicente", "Willa", "Xavier", "Yolanda", "Zeke"]
_2025epachurricanelist = ["Alvin", "Barbara", "Cosme", "Dalila", "Erick", "Flossie", "Gil", "Henriette", "Ivo", "Juliette", "Kiko", "Lorena", "Mario", "Narda", "Octave", "Priscilla", "Raymond", "Sonia", "Tico", "Velma", "Wallis", "Xina", "York", "Zelda"]
_2026epachurricanelist = ["Amanda", "Boris", "Cristina", "Douglas", "Elida", "Fausto", "Genevieve", "Hernan", "Iselle", "Julio", "Karina", "Lowell", "Marie", "Norbert", "Odalys", "Polo", "Rachel", "Simon", "Trudy", "Vance", "Winnie", "Xavier", "Yolanda", "Zeke"]
cpaclist = ["Hone", "Iona", "Keli", "Lala", "Moke", "Nolo", "Olana", "Pena", "Ulana", "Wale ", "Aka", "Ekeka", "Hene", "Iolana", "Keoni", "Lino", "Mele", "Nona", "Oliwa", "Pama", "Upana", "Wene", "Alika", "Ele", "Huko", "Iopa", "Kika", "Lana", "Maka", "Neki", "Omeka", "Pewa", "Unala", "Wali", "Ana", "Ela", "Halola", "Iune", "Kilo", "Loke", "Malia", "Niala", "Oho", "Pali", "Ulika", "Walaka"]
atlauxlist = ["Adria", "Braylen", "Caridad", "Deshawn", "Emery", "Foster", "Gemma", "Heath", "Isla", "Jacobus", "Kenzie", "Lucio", "Makayla", "Nolan", "Orlanda", "Pax", "Ronin", "Sophie", "Tayshaun", "Viviana", "Will"]
epacauxlist = ["Aidan", "Bruna", "Carmelo", "Daniella", "Esteban", "Flor", "Gerardo", "Hedda", "Izzy", "Jacinta", "Kenito", "Luna", "Marina", "Nancy", "Ovidio", "Pia", "Rey", "Skylar", "Teo", "Violeta", "Wilfredo", "Xinia", "Yariel", "Zoe"]


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
            if ts_or_ss > 15 and location not in ["Eastern Pacific", "Central Pacific"]:
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
    if location == "Central Pacific":
        return cpaclist
    if year == 2021:
        if location is None or location == "Atlantic":
            hurricane_list = _2021atlhurricanelist
        elif location == "Eastern Pacific":
            hurricane_list = _2021epachurricanelist
    elif year == 2022:
        if location == "Atlantic":
            hurricane_list = _2022atlhurricanelist
        elif location == "Eastern Pacific":
            hurricane_list = _2022epachurricanelist
    elif year == 2023:
        if location == "Atlantic":
            hurricane_list = _2023atlhurricanelist
        elif location == "Eastern Pacific":
            hurricane_list = _2023epachurricanelist
    elif year == 2024:
        if location == "Atlantic":
            hurricane_list = _2024atlhurricanelist
        elif location == "Eastern Pacific":
            hurricane_list = _2024epachurricanelist
    elif year == 2025:
        if location == "Atlantic":
            hurricane_list = _2025atlhurricanelist
        elif location == "Eastern Pacific":
            hurricane_list = _2025epachurricanelist
    elif year == 2026:
        if location == "Atlantic":
            hurricane_list = _2026atlhurricanelist
        elif location == "Eastern Pacific":
            hurricane_list = _2026epachurricanelist
    if location == "Atlantic":
        return hurricane_list+atlauxlist
    elif location == "Eastern Pacific":
        return hurricane_list+epacauxlist


async def hurricane_amount_calc(la_nina_or_el_nino, cpac=False):
    if cpac is not False:
        return random.randint(1, 10)
    else:
        if la_nina_or_el_nino == 'La Nina':
            return random.randint(5, 36)
        elif la_nina_or_el_nino == 'El Nino':
            return random.randint(2, 13)

months = {"January": {"num": 1},
          "February": {"num": 2},
          "March": {"num": 3},
          "April": {"num": 4},
          "May": {"num": 5},
          "June": {"num": 6},
          "July": {"num": 7},
          "August": {"num": 8},
          "September": {"num": 9},
          "October": {"num": 10},
          "November": {"num": 11},
          "December": {"num": 12}}
