**Scrape individual cars**
----
  Returns json data containing the cars' main attributes and its' value.

* **URL**

  /

* **Method:**

  `POST`
  
*  **URL Params**
    NONE

* **Data Params**
  Awaits an array with the urls of the cars to be processed and/or the html contents of the given urls or other urls. For each url in the urls array and for the urls in the htmls where there is not content provided, the service  E.g.:
  ```json
  {
    "carUrls": ["https://www.hasznaltauto.hu/auto/bmw/x4/bmw_x4_3.5_d_automata_m-packet.x-line.313le-11200623"],
    "htmls": {"https://www.hasznaltauto.hu/szemelyauto/audi/a6/audi_a6_2_0_tdi_ultra_75_000_km_sz_konyv_s_mentes-12769076": "*html_conent*", "http://otherurl.com":""}
  }
  ```
  
* **Success Response:**

  * **Code:** 200 <br />
    **Content:** 
    ```json
    [
      {
        "CarUri":"https://www.hasznaltauto.hu/auto/bmw/x4/bmw_x4_3.5_d_automata_m-packet.x-line.313le-11200623",
        "prod_date":"2014/8",
        "power":"230 kW, 313 LE",
        "price":"13.300.000 Ft",
        "speedometer":"73 000 km",
        "worth": 25.18
      },
      {
        "CarUri":"https://www.hasznaltauto.hu/szemelyauto/audi/a6/audi_a6_2_0_tdi_ultra_75_000_km_sz_konyv_s_mentes-12769076",
        "power":"140 kW",
        "price":"7 199 000 Ft",
        "prod_date":"2014/12",
        "speedometer":"75 000 km",
        "worth": 22
      } ...
     ]
    ```
 
* **Error Response:**
TBD

**Get saved cars**
----
  Returns json data containing the cars' main attributes and its' value.

* **URL**

  /saved-cars

* **Method:**

  `POST`
  
*  **URL Params**
    NONE

* **Data Params**
  A valid logged in google authentication id token. E.g.:
  ```json
    {"idToken":"asdfasdfadfdafdadg123"}
  ```
  
* **Success Response:**

  * **Code:** 200 <br />
    **Content:** 
    ```json
    [
      {
        "CarUri": "url", 
        "power": "221 kW", 
        "speedometer": "34 600 km", 
        "prod_date": "2016/6", 
        "price": "13 390 000 Ft", 
        "worth": 32.79, 
        "linkName": "Audi S3"
      }...
    ]
    ```
 
* **Error Response:**
TBD

**Save cars**
----
  Send car data for save

* **URL**

  /saved-cars

* **Method:**

  `PUT`
  
*  **URL Params**
    NONE

* **Data Params**
  A valid logged in google authentication id token and car data to save with optionally the name that we want to display for the link. E.g.:
  ```json
    {
      "idToken":"asfdaf123",
      "carData":[
        {
          "CarUri":"url",
          "power":"221 kW",
          "speedometer":"34 600 km",
          "prod_date":"2016/6",
          "price":"13 390 000 Ft",
           "worth":32.79,
           "linkName": "Audi S3
      ]
    …
    }
  ```
  
* **Success Response:**

  * **Code:** 200 <br />
    **Content:** 
    ```json
    "Success"
    ```
 
* **Error Response:**
TBD
