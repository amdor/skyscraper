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
