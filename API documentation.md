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

  'id=[integer]'
  'callType=[string]'
  'call_id=[integer]'
  'timestamp=[timestamp]'

  **Optional:**

  'source=[string]'
  'destination=[string]'

* **Success Response:**

  * **Code:** 201 <br/>
    **Content:** 'signaling success'

* **Error Response:**

  * **Code:** 400 Bad Request <br/>
    **Content:** 'id error - input id is not a number'

  OR

  * **Code:** 400 Bad Request <br/>
    **Content:** 'id error - input id is negative'

  OR

  * **Code:** 400 Bad Request <br/>
    **Content:** 'id error - an id already exists'

  OR

  * **Code:** 400 Bad Request <br/>
    **Content:** 'id error - ids from 0 to 100 are reserved'

  OR

  * **Code:** 400 Bad Request <br/>
    **Content:** 'callType error - invalid field'

  OR

  * **Code:** 400 Bad Request <br/>
    **Content:** 'call_id error - input call_id is not a number'

  OR

  * **Code:** 400 Bad Request <br/>
    **Content:** 'call_id error - input call_id is negative'

  OR

  * **Code:** 400 Bad Request <br/>
    **Content:** 'call_id error - ids from 0 to 50 are reserved'

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
    **Content:** 'timestamp error - Invalid timestamp'

  OR

  * **Code:** 400 Bad Request <br/>
    **Content:** 'timing error call timing error, cannot signal
    call end with a timestamp earlier than call start'

* **Payload sample:**
{
    "id": 36,
    "callType": "End",
    "call_id": 19
    "timestamp": "2018-01-04 18:31:38-03:00"
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