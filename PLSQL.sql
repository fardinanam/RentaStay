CREATE OR REPLACE FUNCTION GET_MIN_PRICE(HID IN NUMBER)
RETURN NUMBER IS 
    MIN_PRICE NUMBER;
BEGIN
    SELECT MIN(PRICE) INTO MIN_PRICE
    FROM ROOMS
    WHERE HOUSE_ID = HID;
    
    RETURN MIN_PRICE;
END;
    
CREATE OR REPLACE FUNCTION GET_MAX_PRICE(HID IN NUMBER)
RETURN NUMBER IS 
    MAX_PRICE NUMBER;
BEGIN
    SELECT MAX(PRICE) INTO MAX_PRICE
    FROM ROOMS
    WHERE HOUSE_ID = HID;
    
    RETURN MAX_PRICE;
END;