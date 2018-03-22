**Signaling**
----
    Used to signal a call change of state

* **URL**

  /signaling/

* **Method:**

  'POST'

* **URL Params**

  None

* **Data Params**

  **Required:**

  'recordId=[integer]'
  'callType=[string]'
  'call_id=[integer]'

  **Optional:**

  'source=[string]'
  'destination=[string]'
  'timestamp=[timestamp]'

* **Success Response:**

  * **Code:** 200 <br/>
    **Content:** 'signaling success'

* **Error Response:**

  * **Code:** 400 Bad Request <br/>
    **Content:** 'recordId error - a recordId already exists'

  OR

  * **Code:** 400 Bad Request <br/>
    **Content:** 'callType error - invalid field'

  OR

  * **Code:** 400 Bad Request <br/>
    **Content:** 'call_id error - Call already finished'

  OR

  * **Code:** 400 Bad Request <br/>
    **Content:** 'call_id error - Call already started''

  OR

  * **Code:** 400 Bad Request <br/>
    **Content:** 'call_id error - Call was not started'

  OR

  * **Code:** 400 Bad Request <br/>
    **Content:** 'source error - Invalid source'

  OR

  * **Code:** 400 Bad Request <br/>
    **Content:** 'destination error - Invalid destination'

  OR

  * **Code:** 400 Bad Request <br/>
    **Content:** 'timing error call timing error, cannot signal
    call end with a timestamp earlier than call start'

* **Payload sample:**
{
    "recordId": 36,
    "callType": "End",
    "call_id": 19
}

-----------

**Retrieve bill**
----
    Used to get a month's bill

* **URL**

  /billing/bill

* **Method:**

  'GET'

* **URL Params**

  **Required:**
  'source=[string]'

  **Optional:**
  'year=[string]'
  'month=[string]'

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br/>
    **Content:** '{bill info}'

* **Error Response:**

  * **Code:** 200 <br/>
    **Content:** 'Input error.'

  OR

  * **Code:** 200 <br/>
    **Content:** 'No calls recorded on period.'

* **Call sample:**
GET http://192.168.100.3:8000/billing/bill?source=1234567891&year=2018&month=2