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
  Awaits an array with the urls of the cars to be processed. E.g.:
  ```json
  {
    "carUrls": ["https://www.hasznaltauto.hu/auto/bmw/x4/bmw_x4_3.5_d_automata_m-packet.x-line.313le-11200623"]
  }
  ```
  
* **Success Response:**

  * **Code:** 200 <br />
    **Content:** 
    ```json
    {
      "CarUri":"https://www.hasznaltauto.hu/auto/bmw/x4/bmw_x4_3.5_d_automata_m-packet.x-line.313le-11200623",
      "age":"2014/8",
      "condition":"Újszerű",
      "mass":"1 860 kg",
      "power":"230 kW, 313 LE",
      "price":"13.300.000 Ft",
      "speedometer":"73 000 km",
      "trunk":"500 liter"
    }
    ```
 
* **Error Response:**
TBD
