# coding=utf8
"""
This is an early attempt to extract the country associated with a student by looking at the address
that is entered by the student, extracting some notion of the country, and regularizing that country
(or, in cases of the US, the state). It is at best heuristic, and has been replaced by mechanisms that
use the ip address (taken from the log files) and doing an ip->country lookup, using commercially 
available databases of that information. 

This program is kept around for historical purposes only, and should probably not be used.
"""
import csv
import re
import collections
import os

countryDomains = {".ad": "AD", ".ae": "AE", ".af": "AF", ".ag": "AG", ".ai": "AI", ".al": "AL", ".am": "AM", ".ao": "AO", ".aq": "AQ", ".ar": "AR", ".as": "AS", ".at": "AT", ".au": "AU", ".aw": "AW", ".ax": "AX", ".az": "AZ", ".ba": "BA", ".bb": "BB", ".bd": "BD", ".be": "BE", ".bf": "BF", ".bg": "BG", ".bh": "BH", ".bi": "BI", ".bj": "BJ", ".bl": "BL", ".bm": "BM", ".bn": "BN", ".bo": "BO", ".bq": "BQ", ".br": "BR", ".bs": "BS", ".bt": "BT", ".bv": "BV", ".bw": "BW", ".by": "BY", ".bz": "BZ", ".ca": "CA", ".cc": "CC", ".cd": "CD", ".cf": "CF", ".cg": "CG", ".ch": "CH", ".ci": "CI", ".ck": "CK", ".cl": "CL", ".cm": "CM", ".cn": "CN", ".co": "CO", ".cr": "CR", ".cu": "CU", ".cv": "CV", ".cw": "CW", ".cx": "CX", ".cy": "CY", ".cz": "CZ", ".de": "DE", ".dj": "DJ", ".dk": "DK", ".dm": "DM", ".do": "DO", ".dz": "DZ", ".ec": "EC", ".ee": "EE", ".eg": "EG", ".eh": "EH", ".er": "ER", ".es": "ES", ".et": "ET", ".fi": "FI", ".fj": "FJ", ".fk": "FK", ".fm": "FM", ".fo": "FO", ".fr": "FR", ".ga": "GA", ".gb": "GB", ".uk": "GB", ".gd": "GD", ".ge": "GE", ".gf": "GF", ".gg": "GG", ".gh": "GH", ".gi": "GI", ".gl": "GL", ".gm": "GM", ".gn": "GN", ".gp": "GP", ".gq": "GQ", ".gr": "GR", ".gs": "GS", ".gt": "GT", ".gu": "GU", ".gw": "GW", ".gy": "GY", ".hk": "HK", ".hm": "HM", ".hn": "HN", ".hr": "HR", ".ht": "HT", ".hu": "HU", ".id": "ID", ".ie": "IE", ".il": "IL", ".im": "IM", ".in": "IN", ".io": "IO", ".iq": "IQ", ".ir": "IR", ".is": "IS", ".it": "IT", ".je": "JE", ".jm": "JM", ".jo": "JO", ".jp": "JP", ".ke": "KE", ".kg": "KG", ".kh": "KH", ".ki": "KI", ".km": "KM", ".kn": "KN", ".kp": "KP", ".kr": "KR", ".kw": "KW", ".ky": "KY", ".kz": "KZ", ".la": "LA", ".lb": "LB", ".lc": "LC", ".li": "LI", ".lk": "LK", ".lr": "LR", ".ls": "LS", ".lt": "LT", ".lu": "LU", ".lv": "LV", ".ly": "LY", ".ma": "MA", ".mc": "MC", ".md": "MD", ".me": "ME", ".mf": "MF", ".mg": "MG", ".mh": "MH", ".mk": "MK", ".ml": "ML", ".mm": "MM", ".mn": "MN", ".mo": "MO", ".mp": "MP", ".mq": "MQ", ".mr": "MR", ".ms": "MS", ".mt": "MT", ".mu": "MU", ".mv": "MV", ".mw": "MW", ".mx": "MX", ".my": "MY", ".mz": "MZ", ".na": "NA", ".nc": "NC", ".ne": "NE", ".nf": "NF", ".ng": "NG", ".ni": "NI", ".nl": "NL", ".no": "NO", ".np": "NP", ".nr": "NR", ".nu": "NU", ".nz": "NZ", ".om": "OM", ".pa": "PA", ".pe": "PE", ".pf": "PF", ".pg": "PG", ".ph": "PH", ".pk": "PK", ".pl": "PL", ".pm": "PM", ".pn": "PN", ".pr": "PR", ".ps": "PS", ".pt": "PT", ".pw": "PW", ".py": "PY", ".qa": "QA", ".re": "RE", ".ro": "RO", ".rs": "RS", ".ru": "RU", ".rw": "RW", ".sa": "SA", ".sb": "SB", ".sc": "SC", ".sd": "SD", ".se": "SE", ".sg": "SG", ".sh": "SH", ".si": "SI", ".sj": "SJ", ".sk": "SK", ".sl": "SL", ".sm": "SM", ".sn": "SN", ".so": "SO", ".sr": "SR", ".ss": "SS", ".st": "ST", ".sv": "SV", ".sx": "SX", ".sy": "SY", ".sz": "SZ", ".tc": "TC", ".td": "TD", ".tf": "TF", ".tg": "TG", ".th": "TH", ".tj": "TJ", ".tk": "TK", ".tl": "TL", ".tm": "TM", ".tn": "TN", ".to": "TO", ".tr": "TR", ".tt": "TT", ".tv": "TV", ".tw": "TW", ".tz": "TZ", ".ua": "UA", ".ug": "UG", ".um": "UM", ".us": "US", ".uy": "UY", ".uz": "UZ", ".va": "VA", ".vc": "VC", ".ve": "VE", ".vg": "VG", ".vi": "VI", ".vn": "VN", ".vu": "VU", ".wf": "WF", ".ws": "WS", ".ye": "YE", ".yt": "YT", ".za": "ZA", ".zm": "ZM", ".zw": "ZW", }
countryAbbrvs = {"AD": "Andorra", "AE": "United Arab Emirates", "AF": "Afghanistan", "AG": "Antigua and Barbuda", "AI": "Anguilla", "AL": "Albania", "AM": "Armenia", "AO": "Angola", "AQ": "Antarctica", "AR": "Argentina", "AS": "American Samoa", "AT": "Austria", "AU": "Australia", "AW": "Aruba", "AX": "Aland Islands !", "AZ": "Azerbaijan", "BA": "Bosnia and Herzegovina", "BB": "Barbados", "BD": "Bangladesh", "BE": "Belgium", "BF": "Burkina Faso", "BG": "Bulgaria", "BH": "Bahrain", "BI": "Burundi", "BJ": "Benin", "BL": "Saint Barthélemy", "BM": "Bermuda", "BN": "Brunei Darussalam", "BO": "Bolivia, Plurinational State of", "BQ": "Bonaire, Sint Eustatius and Saba", "BR": "Brazil", "BS": "Bahamas", "BT": "Bhutan", "BV": "Bouvet Island", "BW": "Botswana", "BY": "Belarus", "BZ": "Belize", "CA": "Canada", "CC": "Cocos (Keeling) Islands", "CD": "Congo, the Democratic Republic of the", "CF": "Central African Republic", "CG": "Congo", "CH": "Switzerland", "CI": "Cote d'Ivoire !", "CK": "Cook Islands", "CL": "Chile", "CM": "Cameroon", "CN": "China", "CO": "Colombia", "CR": "Costa Rica", "CU": "Cuba", "CV": "Cape Verde", "CW": "Curaçao", "CX": "Christmas Island", "CY": "Cyprus", "CZ": "Czech Republic", "DE": "Germany", "DJ": "Djibouti", "DK": "Denmark", "DM": "Dominica", "DO": "Dominican Republic", "DZ": "Algeria", "EC": "Ecuador", "EE": "Estonia", "EG": "Egypt", "EH": "Western Sahara", "ER": "Eritrea", "ES": "Spain", "ET": "Ethiopia", "FI": "Finland", "FJ": "Fiji", "FK": "Falkland Islands (Malvinas)", "FM": "Micronesia, Federated States of", "FO": "Faroe Islands", "FR": "France", "GA": "Gabon", "GB": "United Kingdom", "GD": "Grenada", "GE": "Georgia", "GF": "French Guiana", "GG": "Guernsey", "GH": "Ghana", "GI": "Gibraltar", "GL": "Greenland", "GM": "Gambia", "GN": "Guinea", "GP": "Guadeloupe", "GQ": "Equatorial Guinea", "GR": "Greece", "GS": "South Georgia and the South Sandwich Islands", "GT": "Guatemala", "GU": "Guam", "GW": "Guinea-Bissau", "GY": "Guyana", "HK": "Hong Kong", "HM": "Heard Island and McDonald Islands", "HN": "Honduras", "HR": "Croatia", "HT": "Haiti", "HU": "Hungary", "ID": "Indonesia", "IE": "Ireland", "IL": "Israel", "IM": "Isle of Man", "IN": "India", "IO": "British Indian Ocean Territory", "IQ": "Iraq", "IR": "Iran, Islamic Republic of", "IS": "Iceland", "IT": "Italy", "JE": "Jersey", "JM": "Jamaica", "JO": "Jordan", "JP": "Japan", "KE": "Kenya", "KG": "Kyrgyzstan", "KH": "Cambodia", "KI": "Kiribati", "KM": "Comoros", "KN": "Saint Kitts and Nevis", "KP": "Korea, Democratic People's Republic of", "KR": "Korea, Republic of", "KW": "Kuwait", "KY": "Cayman Islands", "KZ": "Kazakhstan", "LA": "Lao People's Democratic Republic", "LB": "Lebanon", "LC": "Saint Lucia", "LI": "Liechtenstein", "LK": "Sri Lanka", "LR": "Liberia", "LS": "Lesotho", "LT": "Lithuania", "LU": "Luxembourg", "LV": "Latvia", "LY": "Libya", "MA": "Morocco", "MC": "Monaco", "MD": "Moldova, Republic of", "ME": "Montenegro", "MF": "Saint Martin (French part)", "MG": "Madagascar", "MH": "Marshall Islands", "MK": "Macedonia, the former Yugoslav Republic of", "ML": "Mali", "MM": "Myanmar", "MN": "Mongolia", "MO": "Macao", "MP": "Northern Mariana Islands", "MQ": "Martinique", "MR": "Mauritania", "MS": "Montserrat", "MT": "Malta", "MU": "Mauritius", "MV": "Maldives", "MW": "Malawi", "MX": "Mexico", "MY": "Malaysia", "MZ": "Mozambique", "NA": "Namibia", "NC": "New Caledonia", "NE": "Niger", "NF": "Norfolk Island", "NG": "Nigeria", "NI": "Nicaragua", "NL": "Netherlands", "NO": "Norway", "NP": "Nepal", "NR": "Nauru", "NU": "Niue", "NZ": "New Zealand", "OM": "Oman", "PA": "Panama", "PE": "Peru", "PF": "French Polynesia", "PG": "Papua New Guinea", "PH": "Philippines", "PK": "Pakistan", "PL": "Poland", "PM": "Saint Pierre and Miquelon", "PN": "Pitcairn", "PR": "Puerto Rico", "PS": "Palestine, State of", "PT": "Portugal", "PW": "Palau", "PY": "Paraguay", "QA": "Qatar", "RE": "Reunion !", "RO": "Romania", "RS": "Serbia", "RU": "Russian Federation", "RW": "Rwanda", "SA": "Saudi Arabia", "SB": "Solomon Islands", "SC": "Seychelles", "SD": "Sudan", "SE": "Sweden", "SG": "Singapore", "SH": "Saint Helena, Ascension and Tristan da Cunha", "SI": "Slovenia", "SJ": "Svalbard and Jan Mayen", "SK": "Slovakia", "SL": "Sierra Leone", "SM": "San Marino", "SN": "Senegal", "SO": "Somalia", "SR": "Suriname", "SS": "South Sudan", "ST": "Sao Tome and Principe", "SV": "El Salvador", "SX": "Sint Maarten (Dutch part)", "SY": "Syrian Arab Republic", "SZ": "Swaziland", "TC": "Turks and Caicos Islands", "TD": "Chad", "TF": "French Southern Territories", "TG": "Togo", "TH": "Thailand", "TJ": "Tajikistan", "TK": "Tokelau", "TL": "Timor-Leste", "TM": "Turkmenistan", "TN": "Tunisia", "TO": "Tonga", "TR": "Turkey", "TT": "Trinidad and Tobago", "TV": "Tuvalu", "TW": "Taiwan, Province of China", "TZ": "Tanzania, United Republic of", "UA": "Ukraine", "UG": "Uganda", "UM": "United States Minor Outlying Islands", "US": "United States", "UY": "Uruguay", "UZ": "Uzbekistan", "VA": "Holy See (Vatican City State)", "VC": "Saint Vincent and the Grenadines", "VE": "Venezuela, Bolivarian Republic of", "VG": "Virgin Islands, British", "VI": "Virgin Islands, U.S.", "VN": "Viet Nam", "VU": "Vanuatu", "WF": "Wallis and Futuna", "WS": "Samoa", "XK": "Kosovo", "YE": "Yemen", "YT": "Mayotte", "ZA": "South Africa", "ZM": "Zambia", "ZW": "Zimbabwe", }
countryNames = {"Andorra": "AD", "United Arab Emirates": "AE", "Afghanistan": "AF", "Antigua and Barbuda": "AG", "Anguilla": "AI", "Albania": "AL", "Armenia": "AM", "Angola": "AO", "Antarctica": "AQ", "Argentina": "AR", "American Samoa": "AS", "Austria": "AT", "Australia": "AU", "Aruba": "AW", "Aland Islands !": "AX", "Azerbaijan": "AZ", "Bosnia and Herzegovina": "BA", "Barbados": "BB", "Bangladesh": "BD", "Belgium": "BE", "Burkina Faso": "BF", "Bulgaria": "BG", "Bahrain": "BH", "Burundi": "BI", "Benin": "BJ", "Saint Barthélemy": "BL", "Bermuda": "BM", "Brunei Darussalam": "BN", "Bolivia, Plurinational State of": "BO", "Bonaire, Sint Eustatius and Saba": "BQ", "Brazil": "BR", "Bahamas": "BS", "Bhutan": "BT", "Bouvet Island": "BV", "Botswana": "BW", "Belarus": "BY", "Belize": "BZ", "Canada": "CA", "Cocos (Keeling) Islands": "CC", "Congo, the Democratic Republic of the": "CD", "Central African Republic": "CF", "Congo": "CG", "Switzerland": "CH", "Cote d'Ivoire !": "CI", "Cook Islands": "CK", "Chile": "CL", "Cameroon": "CM", "China": "CN", "Colombia": "CO", "Costa Rica": "CR", "Cuba": "CU", "Cape Verde": "CV", "Curaçao": "CW", "Christmas Island": "CX", "Cyprus": "CY", "Czech Republic": "CZ", "Germany": "DE", "Djibouti": "DJ", "Denmark": "DK", "Dominica": "DM", "Dominican Republic": "DO", "Algeria": "DZ", "Ecuador": "EC", "Estonia": "EE", "Egypt": "EG", "Western Sahara": "EH", "Eritrea": "ER", "Spain": "ES", "Ethiopia": "ET", "Finland": "FI", "Fiji": "FJ", "Falkland Islands (Malvinas)": "FK", "Micronesia, Federated States of": "FM", "Faroe Islands": "FO", "France": "FR", "Gabon": "GA", "UK": "GB", "United Kingdom": "GB", "Grenada": "GD", "Georgia": "GE", "French Guiana": "GF", "Guernsey": "GG", "Ghana": "GH", "Gibraltar": "GI", "Greenland": "GL", "Gambia": "GM", "Guinea": "GN", "Guadeloupe": "GP", "Equatorial Guinea": "GQ", "Greece": "GR", "South Georgia and the South Sandwich Islands": "GS", "Guatemala": "GT", "Guam": "GU", "Guinea-Bissau": "GW", "Guyana": "GY", "Hong Kong": "HK", "Heard Island and McDonald Islands": "HM", "Honduras": "HN", "Croatia": "HR", "Haiti": "HT", "Hungary": "HU", "Indonesia": "ID", "Ireland": "IE", "Israel": "IL", "Isle of Man": "IM", "India": "IN", "British Indian Ocean Territory": "IO", "Iraq": "IQ", "Iran, Islamic Republic of": "IR", "Iceland": "IS", "Italy": "IT", "Jersey": "JE", "Jamaica": "JM", "Jordan": "JO", "Japan": "JP", "Kenya": "KE", "Kyrgyzstan": "KG", "Cambodia": "KH", "Kiribati": "KI", "Comoros": "KM", "Saint Kitts and Nevis": "KN", "Korea, Democratic People's Republic of": "KP", "Korea, Republic of": "KR", "Kuwait": "KW", "Cayman Islands": "KY", "Kazakhstan": "KZ", "Lao People's Democratic Republic": "LA", "Lebanon": "LB", "Saint Lucia": "LC", "Liechtenstein": "LI", "Sri Lanka": "LK", "Liberia": "LR", "Lesotho": "LS", "Lithuania": "LT", "Luxembourg": "LU", "Latvia": "LV", "Libya": "LY", "Morocco": "MA", "Monaco": "MC", "Moldova, Republic of": "MD", "Montenegro": "ME", "Saint Martin (French part)": "MF", "Madagascar": "MG", "Marshall Islands": "MH", "Macedonia, the former Yugoslav Republic of": "MK", "Mali": "ML", "Myanmar": "MM", "Mongolia": "MN", "Macao": "MO", "Northern Mariana Islands": "MP", "Martinique": "MQ", "Mauritania": "MR", "Montserrat": "MS", "Malta": "MT", "Mauritius": "MU", "Maldives": "MV", "Malawi": "MW", "Mexico": "MX", "Malaysia": "MY", "Mozambique": "MZ", "Namibia": "NA", "New Caledonia": "NC", "Niger": "NE", "Norfolk Island": "NF", "Nigeria": "NG", "Nicaragua": "NI", "Netherlands": "NL", "Norway": "NO", "Nepal": "NP", "Nauru": "NR", "Niue": "NU", "New Zealand": "NZ", "Oman": "OM", "Panama": "PA", "Peru": "PE", "French Polynesia": "PF", "Papua New Guinea": "PG", "Philippines": "PH", "Pakistan": "PK", "Poland": "PL", "Saint Pierre and Miquelon": "PM", "Pitcairn": "PN", "Puerto Rico": "PR", "Palestine, State of": "PS", "Portugal": "PT", "Palau": "PW", "Paraguay": "PY", "Qatar": "QA", "Reunion !": "RE", "Romania": "RO", "Serbia": "RS", "Russian Federation": "RU", "Rwanda": "RW", "Saudi Arabia": "SA", "Solomon Islands": "SB", "Seychelles": "SC", "Sudan": "SD", "Sweden": "SE", "Singapore": "SG", "Saint Helena, Ascension and Tristan da Cunha": "SH", "Slovenia": "SI", "Svalbard and Jan Mayen": "SJ", "Slovakia": "SK", "Sierra Leone": "SL", "San Marino": "SM", "Senegal": "SN", "Somalia": "SO", "Suriname": "SR", "South Sudan": "SS", "Sao Tome and Principe": "ST", "El Salvador": "SV", "Sint Maarten (Dutch part)": "SX", "Syrian Arab Republic": "SY", "Swaziland": "SZ", "Turks and Caicos Islands": "TC", "Chad": "TD", "French Southern Territories": "TF", "Togo": "TG", "Thailand": "TH", "Tajikistan": "TJ", "Tokelau": "TK", "Timor-Leste": "TL", "Turkmenistan": "TM", "Tunisia": "TN", "Tonga": "TO", "Turkey": "TR", "Trinidad and Tobago": "TT", "Tuvalu": "TV", "Taiwan, Province of China": "TW", "Tanzania, United Republic of": "TZ", "Ukraine": "UA", "Uganda": "UG", "United States Minor Outlying Islands": "UM", "United States": "US", "Uruguay": "UY", "Uzbekistan": "UZ", "Holy See (Vatican City State)": "VA", "Saint Vincent and the Grenadines": "VC", "Venezuela, Bolivarian Republic of": "VE", "Virgin Islands, British": "VG", "Virgin Islands, U.S.": "VI", "Viet Nam": "VN", "Vanuatu": "VU", "Wallis and Futuna": "WF", "Samoa": "WS", "Kosovo": "XK", "Yemen": "YE", "Mayotte": "YT", "South Africa": "ZA", "Zambia": "ZM", "Zimbabwe": "ZW", }
nativeCountryNames = {"Brasil": "BR", "中国": "CN", "Republica Dominicana": "DO", "España": "ES"}
usStateAbbrvs = {'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware', 'DC': 'District of Columbia', 'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland', 'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada', 'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York', 'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina', 'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming'}
usCountryAbbrvs = ['US', 'USA']

emailRegex = re.compile(r"^.*@.*(\..*)$")
usAddrRegex = re.compile(r"(?P<addr>.*)[\s|,](?P<state>[a-zA-Z]{2,})[,.]{0,1}\s(?P<zip>\d{5})(?P<plus4>\-\d{4}){0,1}$", re.IGNORECASE|re.DOTALL)
britishPostcodeRegex = re.compile(r"\b(?P<postcode>[A-Z]{1,2}\d{1,2}[A-Z]{0,1} \d[A-Z][A-Z])\b")
indianPINRegex = re.compile(r"\bPIN (?P<PIN>\d{6})\Z", re.IGNORECASE)
countryNameRegexTemplate = r"\b%s\b"
spaceRegex = re.compile(r"[ \t]+")
lastTokenRegex = re.compile(r".*\b(?P<lasttoken>.+)", re.DOTALL)
keyValueRegex = re.compile(r"\"(?P<key>.*)\",\"(?P<value>.*)\"")

def relativePath(relativePath):
    return os.path.join(os.path.dirname(__file__), relativePath)

cities = collections.OrderedDict()
with open(relativePath('data/cities.csv')) as citiesFiles:
    for (city, abbr) in [keyValueRegex.match(line).groups() for line in citiesFiles.readlines()]:
        cities[city] = abbr

def getCountry(loc):
    """
    Extract the country from an address string.
    
    Take an address string, which is self-reported and variously understood as a
    physical mailing address or an email address, and return its corresponding
    ISO 3166-1 alpha-2 country code.
    
    Parameters
    ----------
    loc : string
        A string supplied by the user when asked for a mailing address

    Returns
    -------
    An ISO 3166-1 alpha-2 country code (as a string), or None if unclassifiable
    """

    # if the loc is empty it's unclassifiable
    if loc == '':
        return None

    # clean up whitspace, both removing whitespace from the beginning
    # and end of the string, as well as collapsing multiple spaces to
    # one space anywhere in the string
    loc = spaceRegex.sub(' ', loc.strip())
    
    # check if it's an email address, and extract a country if possible
    emailMatch = emailRegex.match(loc)
    if emailMatch != None:
        domain = emailMatch.group(1)
        if domain in countryDomains:
            return countryDomains[domain]
        else:
            return None
    
    # check if it's a US address
    usAddrMatch = usAddrRegex.match(loc)
    if usAddrMatch != None:
        state = usAddrMatch.group('state')
        if state.upper() == 'PR' or state.upper() == 'PUERTO RICO':
            return 'PR'
        else:
            return 'US'

    # check if it has a UK postcode
    postcodeMatch = britishPostcodeRegex.search(loc)
    if postcodeMatch != None:
        return 'GB'

    # check if it has an Indian PIN
    pinMatch = indianPINRegex.search(loc)
    if pinMatch != None:
        return 'IN'

    # check if a country name is in the address
    for country in countryNames.keys():
        if re.search(countryNameRegexTemplate % country, loc, flags=re.IGNORECASE) != None:
            return countryNames[country]

    # check if a native-language country name is in the address
    for country in nativeCountryNames.keys():
        if re.search(countryNameRegexTemplate % country, loc, flags=re.IGNORECASE) != None:
            return nativeCountryNames[country]

    # check if we can analyze the last token for something special
    lastTokenMatch = lastTokenRegex.match(loc)
    if lastTokenMatch != None:
        lastToken = lastTokenMatch.group('lasttoken').upper()
        if len(lastToken) is 2 and lastToken in usStateAbbrvs or lastToken in usCountryAbbrvs:
            return 'US'

    # deliberately arbitrary... let's call it a heuristic
    if len(loc) >= 20:
        # check if we can find a common city name
        for city in cities.keys():
            if re.search(countryNameRegexTemplate % city, loc, flags=re.IGNORECASE) != None:
                return cities[city]

    return None

if __name__ == '__main__':
    # read in the file that contains the proper classifications for all the test addresses
    classificationsRegex = re.compile(r"^\d{1,3}: (None|[A-Z]{2})$")
    classifications = []
    with open(relativePath('data/countryClassifications.txt')) as classificationsFile:
        for line in classificationsFile.readlines():
            match = classificationsRegex.match(line)
            country = match.group(1)
            if country == 'None':
                classifications.append(None)
            else:
                classifications.append(country)

    # classify the addresses
    with open(relativePath('data/countryTestfileNOPUSH.csv')) as testfile:
        reader = csv.reader(testfile)
        i = 0
        notMatched = 0
        for line in reader:
            if len(line) >= 8:
                country = getCountry(unicode(line[8], 'utf-8'))
                if country != classifications[i]:
                    notMatched += 1
                    print 'Address %s:\n%s\nClassification: %s Correct: %s' % (i, unicode(line[8], 'utf-8'), country, classifications[i])
                    print '-' * 49
                i += 1

        print 'Total addresses: %s' % i
        print 'Correctly classified: %s' % (i - notMatched)
        print 'Incorrectly classified: %s' % notMatched

    with open(relativePath('data/addressListNOPUSH.csv')) as addresses:
        reader = csv.reader(addresses)
        results = {}
        numEmpty = 0
        i = 0
        for line in reader:
            print 'Addr %s' % i
            if unicode(line[0], 'utf-8') == '':
                numEmpty += 1
            country = getCountry(unicode(line[0], 'utf-8'))
            if country in results:
                results[country].append(i)
            else:
                results[country] = [i]
            i += 1
        print results
        print '%s empty entries' % numEmpty
