package demographics

import scala.util.matching.Regex
import java.io.File
import com.github.tototoshi.csv.CSVReader
import scala.collection.mutable.{LinkedHashMap => mLinkedHashMap, Map => mMap, ArrayBuffer => mBuffer}
import scala.collection.immutable.ListMap
import io.Source.fromFile

object getCountry extends App {
  val countryDomains = Map((".ro", "RO"), (".ke", "KE"), (".kg", "KG"), (".kh", "KH"), (".ki", "KI"), (".km", "KM"), (".kn", "KN"), (".kp", "KP"), (".kr", "KR"), (".kw", "KW"), (".rs", "RS"), (".ky", "KY"), (".kz", "KZ"), (".rw", "RW"), (".ru", "RU"), (".bz", "BZ"), (".by", "BY"), (".uz", "UZ"), (".uy", "UY"), (".bs", "BS"), (".br", "BR"), (".bq", "BQ"), (".bw", "BW"), (".bv", "BV"), (".bt", "BT"), (".bj", "BJ"), (".bi", "BI"), (".bh", "BH"), (".bo", "BO"), (".bn", "BN"), (".bm", "BM"), (".bl", "BL"), (".bb", "BB"), (".ba", "BA"), (".bg", "BG"), (".bf", "BF"), (".be", "BE"), (".bd", "BD"), (".eh", "EH"), (".eg", "EG"), (".ee", "EE"), (".ec", "EC"), (".et", "ET"), (".er", "ER"), (".es", "ES"), (".pm", "PM"), (".pl", "PL"), (".pn", "PN"), (".in", "IN"), (".io", "IO"), (".il", "IL"), (".im", "IM"), (".pe", "PE"), (".pg", "PG"), (".pf", "PF"), (".pa", "PA"), (".id", "ID"), (".ie", "IE"), (".py", "PY"), (".ug", "UG"), (".ir", "IR"), (".is", "IS"), (".pw", "PW"), (".iq", "IQ"), (".it", "IT"), (".pr", "PR"), (".sc", "SC"), (".sx", "SX"), (".sy", "SY"), (".ye", "YE"), (".om", "OM"), (".vu", "VU"), (".vg", "VG"), (".ve", "VE"), (".tz", "TZ"), (".vc", "VC"), (".va", "VA"), (".vn", "VN"), (".vi", "VI"), (".fo", "FO"), (".fm", "FM"), (".fk", "FK"), (".fj", "FJ"), (".fi", "FI"), (".fr", "FR"), (".tr", "TR"), (".re", "RE"), (".tw", "TW"), (".tv", "TV"), (".th", "TH"), (".tk", "TK"), (".yt", "YT"), (".tj", "TJ"), (".tl", "TL"), (".mv", "MV"), (".mw", "MW"), (".mt", "MT"), (".mu", "MU"), (".mr", "MR"), (".ms", "MS"), (".mp", "MP"), (".mq", "MQ"), (".tn", "TN"), (".mz", "MZ"), (".tt", "TT"), (".mx", "MX"), (".my", "MY"), (".mf", "MF"), (".mg", "MG"), (".md", "MD"), (".me", "ME"), (".tm", "TM"), (".mc", "MC"), (".to", "TO"), (".ma", "MA"), (".mn", "MN"), (".mo", "MO"), (".ml", "ML"), (".mm", "MM"), (".mk", "MK"), (".mh", "MH"), (".tf", "TF"), (".dk", "DK"), (".dj", "DJ"), (".dm", "DM"), (".do", "DO"), (".de", "DE"), (".td", "TD"), (".dz", "DZ"), (".tg", "TG"), (".us", "US"), (".tc", "TC"), (".um", "UM"), (".uk", "GB"), (".cx", "CX"), (".cy", "CY"), (".cz", "CZ"), (".cr", "CR"), (".cu", "CU"), (".cv", "CV"), (".cw", "CW"), (".ch", "CH"), (".ci", "CI"), (".ck", "CK"), (".cl", "CL"), (".cm", "CM"), (".cn", "CN"), (".co", "CO"), (".ca", "CA"), (".cc", "CC"), (".cd", "CD"), (".cf", "CF"), (".cg", "CG"), (".zw", "ZW"), (".za", "ZA"), (".ua", "UA"), (".zm", "ZM"), (".je", "JE"), (".jo", "JO"), (".jm", "JM"), (".jp", "JP"), (".ws", "WS"), (".sh", "SH"), (".si", "SI"), (".sj", "SJ"), (".sk", "SK"), (".sl", "SL"), (".sm", "SM"), (".sn", "SN"), (".so", "SO"), (".hm", "HM"), (".sa", "SA"), (".sb", "SB"), (".hn", "HN"), (".sd", "SD"), (".se", "SE"), (".hk", "HK"), (".sg", "SG"), (".hu", "HU"), (".ht", "HT"), (".sz", "SZ"), (".hr", "HR"), (".sr", "SR"), (".ss", "SS"), (".st", "ST"), (".sv", "SV"), (".wf", "WF"), (".ph", "PH"), (".pk", "PK"), (".no", "NO"), (".nl", "NL"), (".ni", "NI"), (".ng", "NG"), (".nf", "NF"), (".ne", "NE"), (".nc", "NC"), (".na", "NA"), (".qa", "QA"), (".nz", "NZ"), (".nu", "NU"), (".nr", "NR"), (".np", "NP"), (".af", "AF"), (".ag", "AG"), (".ad", "AD"), (".ae", "AE"), (".ai", "AI"), (".ao", "AO"), (".al", "AL"), (".am", "AM"), (".ar", "AR"), (".as", "AS"), (".aq", "AQ"), (".aw", "AW"), (".at", "AT"), (".au", "AU"), (".az", "AZ"), (".ax", "AX"), (".pt", "PT"), (".ps", "PS"), (".ls", "LS"), (".lr", "LR"), (".lu", "LU"), (".lt", "LT"), (".lv", "LV"), (".ly", "LY"), (".la", "LA"), (".lc", "LC"), (".lb", "LB"), (".li", "LI"), (".lk", "LK"), (".gd", "GD"), (".ge", "GE"), (".gf", "GF"), (".gg", "GG"), (".ga", "GA"), (".gb", "GB"), (".gl", "GL"), (".gm", "GM"), (".gn", "GN"), (".gh", "GH"), (".gi", "GI"), (".gt", "GT"), (".gu", "GU"), (".gw", "GW"), (".gp", "GP"), (".gq", "GQ"), (".gr", "GR"), (".gs", "GS"), (".gy", "GY"))
  val countryAbbrvs = Map(("WF", "Wallis and Futuna"), ("JP", "Japan"), ("JM", "Jamaica"), ("JO", "Jordan"), ("WS", "Samoa"), ("JE", "Jersey"), ("GW", "Guinea-Bissau"), ("GU", "Guam"), ("GT", "Guatemala"), ("GS", "South Georgia and the South Sandwich Islands"), ("GR", "Greece"), ("GQ", "Equatorial Guinea"), ("GP", "Guadeloupe"), ("GY", "Guyana"), ("GG", "Guernsey"), ("GF", "French Guiana"), ("GE", "Georgia"), ("GD", "Grenada"), ("GB", "United Kingdom"), ("GA", "Gabon"), ("GN", "Guinea"), ("GM", "Gambia"), ("GL", "Greenland"), ("GI", "Gibraltar"), ("GH", "Ghana"), ("PR", "Puerto Rico"), ("PS", "Palestine, State of"), ("PW", "Palau"), ("PT", "Portugal"), ("PY", "Paraguay"), ("PA", "Panama"), ("PF", "French Polynesia"), ("PG", "Papua New Guinea"), ("PE", "Peru"), ("PK", "Pakistan"), ("PH", "Philippines"), ("PN", "Pitcairn"), ("PL", "Poland"), ("PM", "Saint Pierre and Miquelon"), ("ZM", "Zambia"), ("ZA", "South Africa"), ("ZW", "Zimbabwe"), ("ME", "Montenegro"), ("MD", "Moldova, Republic of"), ("MG", "Madagascar"), ("MF", "Saint Martin (French part)"), ("MA", "Morocco"), ("MC", "Monaco"), ("MM", "Myanmar"), ("ML", "Mali"), ("MO", "Macao"), ("MN", "Mongolia"), ("MH", "Marshall Islands"), ("MK", "Macedonia, the former Yugoslav Republic of"), ("MU", "Mauritius"), ("MT", "Malta"), ("MW", "Malawi"), ("MV", "Maldives"), ("MQ", "Martinique"), ("MP", "Northern Mariana Islands"), ("MS", "Montserrat"), ("MR", "Mauritania"), ("MY", "Malaysia"), ("MX", "Mexico"), ("MZ", "Mozambique"), ("FR", "France"), ("FI", "Finland"), ("FJ", "Fiji"), ("FK", "Falkland Islands (Malvinas)"), ("FM", "Micronesia, Federated States of"), ("FO", "Faroe Islands"), ("CK", "Cook Islands"), ("CI", "Cote d'Ivoire"), ("CH", "Switzerland"), ("CO", "Colombia"), ("CN", "China"), ("CM", "Cameroon"), ("CL", "Chile"), ("CC", "Cocos (Keeling) Islands"), ("CA", "Canada"), ("CG", "Congo"), ("CF", "Central African Republic"), ("CD", "Congo, the Democratic Republic of the"), ("CZ", "Czech Republic"), ("CY", "Cyprus"), ("CX", "Christmas Island"), ("CR", "Costa Rica"), ("CW", "Curaçao"), ("CV", "Cape Verde"), ("CU", "Cuba"), ("SZ", "Swaziland"), ("SY", "Syrian Arab Republic"), ("SX", "Sint Maarten (Dutch part)"), ("SS", "South Sudan"), ("SR", "Suriname"), ("SV", "El Salvador"), ("ST", "Sao Tome and Principe"), ("SK", "Slovakia"), ("SJ", "Svalbard and Jan Mayen"), ("SI", "Slovenia"), ("SH", "Saint Helena, Ascension and Tristan da Cunha"), ("SO", "Somalia"), ("SN", "Senegal"), ("SM", "San Marino"), ("SL", "Sierra Leone"), ("SC", "Seychelles"), ("SB", "Solomon Islands"), ("SA", "Saudi Arabia"), ("SG", "Singapore"), ("SE", "Sweden"), ("SD", "Sudan"), ("YE", "Yemen"), ("YT", "Mayotte"), ("LB", "Lebanon"), ("LC", "Saint Lucia"), ("LA", "Lao People's Democratic Republic"), ("LK", "Sri Lanka"), ("LI", "Liechtenstein"), ("LV", "Latvia"), ("LT", "Lithuania"), ("LU", "Luxembourg"), ("LR", "Liberia"), ("LS", "Lesotho"), ("LY", "Libya"), ("VA", "Holy See (Vatican City State)"), ("VC", "Saint Vincent and the Grenadines"), ("VE", "Venezuela, Bolivarian Republic of"), ("VG", "Virgin Islands, British"), ("IQ", "Iraq"), ("VI", "Virgin Islands, U.S."), ("IS", "Iceland"), ("IR", "Iran, Islamic Republic of"), ("IT", "Italy"), ("VN", "Viet Nam"), ("IM", "Isle of Man"), ("IL", "Israel"), ("IO", "British Indian Ocean Territory"), ("IN", "India"), ("IE", "Ireland"), ("ID", "Indonesia"), ("BD", "Bangladesh"), ("BE", "Belgium"), ("BF", "Burkina Faso"), ("BG", "Bulgaria"), ("BA", "Bosnia and Herzegovina"), ("BB", "Barbados"), ("BL", "Saint Barthélemy"), ("BM", "Bermuda"), ("BN", "Brunei Darussalam"), ("BO", "Bolivia, Plurinational State of"), ("BH", "Bahrain"), ("BI", "Burundi"), ("BJ", "Benin"), ("BT", "Bhutan"), ("BV", "Bouvet Island"), ("BW", "Botswana"), ("BQ", "Bonaire, Sint Eustatius and Saba"), ("BR", "Brazil"), ("BS", "Bahamas"), ("BY", "Belarus"), ("BZ", "Belize"), ("RU", "Russian Federation"), ("RW", "Rwanda"), ("RS", "Serbia"), ("RE", "Reunion"), ("RO", "Romania"), ("OM", "Oman"), ("HR", "Croatia"), ("HT", "Haiti"), ("HU", "Hungary"), ("HK", "Hong Kong"), ("HN", "Honduras"), ("HM", "Heard Island and McDonald Islands"), ("EH", "Western Sahara"), ("EE", "Estonia"), ("EG", "Egypt"), ("EC", "Ecuador"), ("ET", "Ethiopia"), ("ES", "Spain"), ("ER", "Eritrea"), ("UY", "Uruguay"), ("UZ", "Uzbekistan"), ("US", "United States"), ("UM", "United States Minor Outlying Islands"), ("UG", "Uganda"), ("UA", "Ukraine"), ("VU", "Vanuatu"), ("NI", "Nicaragua"), ("NL", "Netherlands"), ("NO", "Norway"), ("NA", "Namibia"), ("NC", "New Caledonia"), ("NE", "Niger"), ("NF", "Norfolk Island"), ("NG", "Nigeria"), ("NZ", "New Zealand"), ("NP", "Nepal"), ("NR", "Nauru"), ("NU", "Niue"), ("XK", "Kosovo"), ("KG", "Kyrgyzstan"), ("KE", "Kenya"), ("KI", "Kiribati"), ("KH", "Cambodia"), ("KN", "Saint Kitts and Nevis"), ("KM", "Comoros"), ("KR", "Korea, Republic of"), ("KP", "Korea, Democratic People's Republic of"), ("KW", "Kuwait"), ("KZ", "Kazakhstan"), ("KY", "Cayman Islands"), ("DO", "Dominican Republic"), ("DM", "Dominica"), ("DJ", "Djibouti"), ("DK", "Denmark"), ("DE", "Germany"), ("DZ", "Algeria"), ("TZ", "Tanzania, United Republic of"), ("TV", "Tuvalu"), ("TW", "Taiwan, Province of China"), ("TT", "Trinidad and Tobago"), ("TR", "Turkey"), ("TN", "Tunisia"), ("TO", "Tonga"), ("TL", "Timor-Leste"), ("TM", "Turkmenistan"), ("TJ", "Tajikistan"), ("TK", "Tokelau"), ("TH", "Thailand"), ("TF", "French Southern Territories"), ("TG", "Togo"), ("TD", "Chad"), ("TC", "Turks and Caicos Islands"), ("AE", "United Arab Emirates"), ("AD", "Andorra"), ("AG", "Antigua and Barbuda"), ("AF", "Afghanistan"), ("AI", "Anguilla"), ("AM", "Armenia"), ("AL", "Albania"), ("AO", "Angola"), ("AQ", "Antarctica"), ("AS", "American Samoa"), ("AR", "Argentina"), ("AU", "Australia"), ("AT", "Austria"), ("AW", "Aruba"), ("AX", "Aland Islands"), ("AZ", "Azerbaijan"), ("QA", "Qatar"))
  val countryNames = Map(("Canada", "CA"), ("Turkmenistan", "TM"), ("Iran, Islamic Republic of", "IR"), ("Saint Pierre and Miquelon", "PM"), ("Ethiopia", "ET"), ("Swaziland", "SZ"), ("Cameroon", "CM"), ("Burkina Faso", "BF"), ("United States Minor Outlying Islands", "UM"), ("Cocos (Keeling) Islands", "CC"), ("Bosnia and Herzegovina", "BA"), ("Russian Federation", "RU"), ("Bonaire, Sint Eustatius and Saba", "BQ"), ("Dominica", "DM"), ("Liberia", "LR"), ("Maldives", "MV"), ("Christmas Island", "CX"), ("Monaco", "MC"), ("Wallis and Futuna", "WF"), ("Jersey", "JE"), ("Svalbard and Jan Mayen", "SJ"), ("Macao", "MO"), ("Turkey", "TR"), ("Afghanistan", "AF"), ("France", "FR"), ("Slovakia", "SK"), ("Vanuatu", "VU"), ("Nauru", "NR"), ("Seychelles", "SC"), ("Norway", "NO"), ("Malawi", "MW"), ("Congo, the Democratic Republic of the", "CD"), ("Montenegro", "ME"), ("Micronesia, Federated States of", "FM"), ("Timor-Leste", "TL"), ("Dominican Republic", "DO"), ("Bahrain", "BH"), ("Cayman Islands", "KY"), ("Libya", "LY"), ("Finland", "FI"), ("Central African Republic", "CF"), ("Reunion", "RE"), ("Liechtenstein", "LI"), ("United States", "US"), ("Portugal", "PT"), ("Fiji", "FJ"), ("Venezuela, Bolivarian Republic of", "VE"), ("Malaysia", "MY"), ("Pitcairn", "PN"), ("Guinea", "GN"), ("Panama", "PA"), ("Korea, Republic of", "KR"), ("Costa Rica", "CR"), ("Luxembourg", "LU"), ("American Samoa", "AS"), ("Andorra", "AD"), ("Gibraltar", "GI"), ("Ireland", "IE"), ("Palau", "PW"), ("Nigeria", "NG"), ("Ecuador", "EC"), ("Australia", "AU"), ("El Salvador", "SV"), ("Tuvalu", "TV"), ("Rwanda", "RW"), ("Thailand", "TH"), ("Belize", "BZ"), ("Hong Kong", "HK"), ("Sierra Leone", "SL"), ("Aland Islands", "AX"), ("Georgia", "GE"), ("Lao People's Democratic Republic", "LA"), ("Denmark", "DK"), ("Philippines", "PH"), ("Morocco", "MA"), ("Guernsey", "GG"), ("Estonia", "EE"), ("Kosovo", "XK"), ("Curaçao", "CW"), ("Lebanon", "LB"), ("Uzbekistan", "UZ"), ("Falkland Islands (Malvinas)", "FK"), ("Holy See (Vatican City State)", "VA"), ("Colombia", "CO"), ("Cyprus", "CY"), ("Barbados", "BB"), ("Madagascar", "MG"), ("Italy", "IT"), ("Sudan", "SD"), ("Bolivia, Plurinational State of", "BO"), ("Nepal", "NP"), ("Mayotte", "YT"), ("Netherlands", "NL"), ("Suriname", "SR"), ("Anguilla", "AI"), ("Israel", "IL"), ("Senegal", "SN"), ("Papua New Guinea", "PG"), ("Zimbabwe", "ZW"), ("Jordan", "JO"), ("Martinique", "MQ"), ("Moldova, Republic of", "MD"), ("Mauritania", "MR"), ("Uganda", "UG"), ("Trinidad and Tobago", "TT"), ("Latvia", "LV"), ("Japan", "JP"), ("Guadeloupe", "GP"), ("Mexico", "MX"), ("Serbia", "RS"), ("United Kingdom", "GB"), ("Congo", "CG"), ("Korea, Democratic People's Republic of", "KP"), ("Paraguay", "PY"), ("French Guiana", "GF"), ("Botswana", "BW"), ("Sao Tome and Principe", "ST"), ("Lithuania", "LT"), ("Cambodia", "KH"), ("Saint Helena, Ascension and Tristan da Cunha", "SH"), ("Aruba", "AW"), ("Argentina", "AR"), ("Ghana", "GH"), ("Saudi Arabia", "SA"), ("Cape Verde", "CV"), ("Slovenia", "SI"), ("Guatemala", "GT"), ("Kuwait", "KW"), ("Virgin Islands, British", "VG"), ("Spain", "ES"), ("Pakistan", "PK"), ("Oman", "OM"), ("Greenland", "GL"), ("Gabon", "GA"), ("Niue", "NU"), ("Bahamas", "BS"), ("New Zealand", "NZ"), ("Yemen", "YE"), ("Jamaica", "JM"), ("Albania", "AL"), ("Samoa", "WS"), ("Norfolk Island", "NF"), ("United Arab Emirates", "AE"), ("Guam", "GU"), ("India", "IN"), ("Azerbaijan", "AZ"), ("Lesotho", "LS"), ("Saint Vincent and the Grenadines", "VC"), ("Kenya", "KE"), ("Czech Republic", "CZ"), ("Eritrea", "ER"), ("Solomon Islands", "SB"), ("Turks and Caicos Islands", "TC"), ("Saint Lucia", "LC"), ("San Marino", "SM"), ("Mongolia", "MN"), ("Macedonia, the former Yugoslav Republic of", "MK"), ("Syrian Arab Republic", "SY"), ("Bermuda", "BM"), ("Somalia", "SO"), ("Peru", "PE"), ("Cote d'Ivoire", "CI"), ("Benin", "BJ"), ("Cuba", "CU"), ("Saint Kitts and Nevis", "KN"), ("Togo", "TG"), ("China", "CN"), ("Armenia", "AM"), ("Ukraine", "UA"), ("Tonga", "TO"), ("Western Sahara", "EH"), ("Indonesia", "ID"), ("Mauritius", "MU"), ("Sweden", "SE"), ("Mali", "ML"), ("Bulgaria", "BG"), ("Palestine, State of", "PS"), ("Romania", "RO"), ("Angola", "AO"), ("French Southern Territories", "TF"), ("Chad", "TD"), ("South Africa", "ZA"), ("Tokelau", "TK"), ("Tajikistan", "TJ"), ("South Georgia and the South Sandwich Islands", "GS"), ("Brunei Darussalam", "BN"), ("Qatar", "QA"), ("Austria", "AT"), ("Mozambique", "MZ"), ("UK", "GB"), ("Hungary", "HU"), ("Niger", "NE"), ("Brazil", "BR"), ("Faroe Islands", "FO"), ("Virgin Islands, U.S.", "VI"), ("Bangladesh", "BD"), ("Viet Nam", "VN"), ("Belarus", "BY"), ("Algeria", "DZ"), ("Marshall Islands", "MH"), ("Chile", "CL"), ("Puerto Rico", "PR"), ("Belgium", "BE"), ("Kiribati", "KI"), ("Haiti", "HT"), ("Iraq", "IQ"), ("Gambia", "GM"), ("Namibia", "NA"), ("French Polynesia", "PF"), ("Guinea-Bissau", "GW"), ("Switzerland", "CH"), ("Grenada", "GD"), ("Taiwan, Province of China", "TW"), ("Isle of Man", "IM"), ("Tanzania, United Republic of", "TZ"), ("Uruguay", "UY"), ("Saint Barthélemy", "BL"), ("Equatorial Guinea", "GQ"), ("Tunisia", "TN"), ("Djibouti", "DJ"), ("Heard Island and McDonald Islands", "HM"), ("Antigua and Barbuda", "AG"), ("Burundi", "BI"), ("Nicaragua", "NI"), ("Saint Martin (French part)", "MF"), ("Bhutan", "BT"), ("Malta", "MT"), ("Northern Mariana Islands", "MP"), ("Bouvet Island", "BV"), ("Iceland", "IS"), ("Zambia", "ZM"), ("Germany", "DE"), ("Cook Islands", "CK"), ("Kazakhstan", "KZ"), ("Poland", "PL"), ("Kyrgyzstan", "KG"), ("Greece", "GR"), ("British Indian Ocean Territory", "IO"), ("Montserrat", "MS"), ("New Caledonia", "NC"), ("South Sudan", "SS"), ("Guyana", "GY"), ("Honduras", "HN"), ("Myanmar", "MM"), ("Egypt", "EG"), ("Singapore", "SG"), ("Antarctica", "AQ"), ("Sint Maarten (Dutch part)", "SX"), ("Sri Lanka", "LK"), ("Croatia", "HR"), ("Comoros", "KM"))
  val nativeCountryNames = Map(("中国", "CN"), ("España", "ES"), ("Republica Dominicana", "DO"), ("Brasil", "BR"))
  val usStateAbbrvs = Map(("WA", "Washington"), ("WI", "Wisconsin"), ("WV", "West Virginia"), ("FL", "Florida"), ("WY", "Wyoming"), ("NH", "New Hampshire"), ("NJ", "New Jersey"), ("NM", "New Mexico"), ("NC", "North Carolina"), ("ND", "North Dakota"), ("NE", "Nebraska"), ("NY", "New York"), ("RI", "Rhode Island"), ("NV", "Nevada"), ("CO", "Colorado"), ("CA", "California"), ("GA", "Georgia"), ("CT", "Connecticut"), ("OK", "Oklahoma"), ("OH", "Ohio"), ("KS", "Kansas"), ("SC", "South Carolina"), ("KY", "Kentucky"), ("OR", "Oregon"), ("SD", "South Dakota"), ("DE", "Delaware"), ("DC", "District of Columbia"), ("HI", "Hawaii"), ("TX", "Texas"), ("LA", "Louisiana"), ("TN", "Tennessee"), ("PA", "Pennsylvania"), ("VA", "Virginia"), ("AK", "Alaska"), ("AL", "Alabama"), ("AR", "Arkansas"), ("VT", "Vermont"), ("IL", "Illinois"), ("IN", "Indiana"), ("IA", "Iowa"), ("AZ", "Arizona"), ("ID", "Idaho"), ("ME", "Maine"), ("MD", "Maryland"), ("MA", "Massachusetts"), ("UT", "Utah"), ("MO", "Missouri"), ("MN", "Minnesota"), ("MI", "Michigan"), ("MT", "Montana"))
  val usCountryAbbrvs = List("US", "USA")

  val emailRegex = new Regex("""^.*@.*(\..*)$""")
  val usAddrRegex = new Regex("""(?is)(.*)[\s|,]([a-zA-Z]{2,})[,.]{0,1}\s(\d{5})(\-\d{4}){0,1}$""", 
    "Address", "State", "Zip", "Plus4")
  val britishPostcodeRegex = new Regex("""\b([A-Z]{1,2}\d{1,2}[A-Z]{0,1} \d[A-Z][A-Z])\b""", "Postcode")
  val indianPINRegex = new Regex("""(?i)\bPIN (\d{6})\Z""", "PIN")
  def countryRegex(country: String) = ("""(?i)\b""" + country + """\b""").r
  val spaceRegex = new Regex("""[ \t]+""")
  val lastTokenRegex = new Regex("""(?s).*\b(.+)""", "LastToken")
  val keyValueRegex = new Regex("""\"(.*)\",\"(.*)\"""", /*"*/ "Key", "Value")

  var classifications = mBuffer[String]()
  var cities          = mLinkedHashMap[String, String]()

  var notMatched      = 0
  var i               = 0

  /* read in the cities */
  fromFile("data/cities.csv").getLines.foreach { line =>
    val keyValueRegex(city, abbr) = line
    cities(city) = abbr
  }

  /* read in the correct classifications for the test data */
  for (line <- fromFile("data/countryClassifications.txt").getLines)
    classifications += line.split(": ")(1)

  /* classify the test data */
  // for {
  //   line <- CSVReader.open(new File("data/countryTestfileNOPUSH.csv")).all
  //   if (line.length) >= 8
  // } {
  //   val country = getCountry(line(8))
  //   if (country != classifications(i)) {
  //     notMatched += 1
  //     println(s"Address $i:\n${line(8)}\nClassification: $country Correct: ${classifications(i)}")
  //     println("-" * 49)
  //   }

  //   i += 1
  // }

  // println(s"Total addresses: $i")
  // println(s"Correctly classified: ${i - notMatched}")
  // println(s"Incorrectly classified: $notMatched")

  /* classify the big data set */
  var results = mMap[String, mBuffer[Int]]()
  var numEmpty = 0
  i = 0
  for (line <- CSVReader.open(new File("data/addressListNOPUSH.csv")).all) {
    // println(s"Address $i")

    // if (i == 10426) {
      if (line(0) equals "") numEmpty += 1

      // TODO remove
      // println(line(0))

      val country = getCountry(line(0))

      if (results contains country)
        results(country) += i
      else
        results(country) = mBuffer(i)
    // }

    i += 1
  }

  /* print out the results like a Python dictionary */
  var lists = mBuffer[String]()
  for (item <- results.toList) {
    lists += "'%s': %s".format(item._1, item._2.mkString("[", ", ", "]"))
  }
  println(lists.mkString("{", ", ", "}"))

  // for (item <- results.toList.sortBy{-_._2}) {
  //   if (countryAbbrvs contains item._1)
  //     println("%s (%s) %s".format(item._1, countryAbbrvs(item._1), item._2))
  //   else
  //     println("%s %s".format(item._1, item._2))
  // }

  println(s"$numEmpty empty entries")

  def getCountry(location: String): String = {
    /* if the loc is empty it's unclassifiable */
    if (location == "") return "None"

    /* clean up whitespace, both removing whitespace from the beginning
       and end of the string, as well as collapsing multiple spaces to
       one space anywhere in the string */
    val locationNew = spaceRegex replaceAllIn(location.trim, " ")

    /* check if it's an email address */
    locationNew match {
      case emailRegex(domain) =>
        if (countryDomains contains domain) return countryDomains(domain) else return "None"
      case _ =>
    }

    /* check if it's a US address */
    locationNew match {
      case usAddrRegex(address, state, zip, plus4) =>
        if (state.toUpperCase == "PR" || state.toUpperCase == "PUERTO RICO")
          return "PR"
        else
          return "US"
      case _ =>
    }

    /* check if it has a UK postcode */
    britishPostcodeRegex findFirstIn locationNew match {
      case Some(_) => return "GB"
      case None =>
    }

    /* check if it has an Indian PIN */
    indianPINRegex findFirstIn locationNew match {
      case Some(_) => return "IN"
      case None =>
    }

    /* check if a country name is in the address */
    for (country <- countryNames.keys) {
      val regex = countryRegex(country)
      regex findFirstIn locationNew match {
        case Some(_) => return countryNames(country)
        case None =>
      }
    }

    /* check if a native-language country name is in the address */
    for (country <- nativeCountryNames.keys) {
      val regex = countryRegex(country)
      regex findFirstIn locationNew match {
        case Some(_) => return nativeCountryNames(country)
        case None =>
      }
    }

    /* check if we can analyze the last token for something special */
    locationNew match {
      case lastTokenRegex(lastToken) =>
        val lastTokenUpper = lastToken.toUpperCase
        if (lastTokenUpper.length == 2 && (usStateAbbrvs contains lastTokenUpper) || (usCountryAbbrvs contains lastTokenUpper)) return "US"
      case _ =>
    }

    /* try to find a common city name */
    if ((locationNew.length) >= 20) {
      for ((city, country) <- cities) {
        countryRegex(city).findFirstIn(locationNew) match {
          case Some(_) => return country
          case None =>
        }
      }
    }

    return "None"
  }
}
