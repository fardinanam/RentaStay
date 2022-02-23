--Sawraz

-- Function to check if there is any rent currently going on under any house  
CREATE OR REPLACE FUNCTION GET_LAST_DATE_HOUSE(HID IN NUMBER)
RETURN BOOLEAN IS 
    LAST_DATE DATE;
BEGIN
    SELECT MAX(CHECKOUT) INTO LAST_DATE
    FROM RENTS
    WHERE HOUSE_ID = HID;
    IF LAST_DATE>=SYSDATE THEN
			DBMS_OUTPUT.PUT_LINE('Rent Exist');
			RETURN TRUE;
		ELSE
			DBMS_OUTPUT.PUT_LINE('Rent not exist');
			RETURN FALSE;
		END IF;
END;

-- Function to check if there is any rent currently going on under any room  
CREATE OR REPLACE FUNCTION GET_LAST_DATE_ROOM(HID IN NUMBER, RID IN NUMBER)
RETURN BOOLEAN IS 
		LAST_DATE DATE; 
BEGIN
    SELECT MAX(CHECKOUT) INTO LAST_DATE
    FROM RENTS
    WHERE HOUSE_ID = HID AND ROOM_NO = RID;
    IF LAST_DATE>=SYSDATE THEN
			DBMS_OUTPUT.PUT_LINE('Rent Exist');
			RETURN TRUE;
		ELSE
			DBMS_OUTPUT.PUT_LINE('Rent not exist');
			RETURN FALSE;
		END IF;
END;

-- Function to check if there is any rent currently going on under any user  
CREATE OR REPLACE FUNCTION GET_LAST_DATE_USER(UID IN NUMBER)
RETURN BOOLEAN IS 
		LAST_DATE DATE; 
BEGIN
    SELECT MAX(CHECKOUT) INTO LAST_DATE
    FROM RENTS
    WHERE USER_ID = UID;
    IF LAST_DATE>=SYSDATE THEN
			DBMS_OUTPUT.PUT_LINE('Rent Exist');
			RETURN TRUE;
		ELSE
			DBMS_OUTPUT.PUT_LINE('Rent not exist');
			RETURN FALSE;
		END IF;
END;




--Aungon--
ALTER TABLE USERS
ADD IS_HOST NUMBER(1);

ALTER TABLE USERS
ADD JOIN_DATE DATE;

UPDATE USERS
SET IS_HOST = 1
WHERE USER_ID IN (SELECT USER_ID FROM HOUSES);

CREATE TABLE DEPOSITS (
    USER_ID NUMBER,
    TRANSACTION_ID VARCHAR2(50) UNIQUE,
    BANK_ACC_NO VARCHAR2(35),
    
    CONSTRAINTS DEPOSITS_USER_FK FOREIGN KEY(USER_ID) REFERENCES USERS(USER_ID),
    CONSTRAINTS DEPOSITS_PAYMENTS_FK FOREIGN KEY(TRANSACTION_ID) REFERENCES PAYMENTS(TRANSACTION_ID)
);

CREATE OR REPLACE TRIGGER UPDATE_DEPOSITS
FOR INSERT
ON RENTS
COMPOUND TRIGGER
    UID NUMBER;
    USER_BANK_ACC_NO VARCHAR2(35);

    BEFORE EACH ROW IS
    BEGIN
        SELECT BANK_ACC_NO INTO USER_BANK_ACC_NO
        FROM USERS WHERE USER_ID = :NEW.USER_ID;
        
        IF USER_BANK_ACC_NO IS NULL THEN
            RAISE_APPLICATION_ERROR(-20001, 'Transaction cant be completed. User doesnt have bank account no');
        END IF;
    END BEFORE EACH ROW;

    AFTER EACH ROW IS
    BEGIN
        SELECT USER_ID INTO UID
        FROM HOUSES WHERE HOUSE_ID = :NEW.HOUSE_ID;
        
        INSERT INTO DEPOSITS
        VALUES(UID, :NEW.TRANSACTION_ID, USER_BANK_ACC_NO);
    END AFTER EACH ROW;
END;

ALTER TABLE HOUSES
MODIFY DESCRIPTION VARCHAR2(512);

CREATE OR REPLACE TRIGGER MAKE_HOST
AFTER INSERT
ON HOUSES
FOR EACH ROW
DECLARE
    ISHOST NUMBER(1);
BEGIN
    DBMS_OUTPUT.PUT_LINE('Make host triggered ' || :NEW.USER_ID);
    UPDATE USERS
    SET IS_HOST = 1
    WHERE USER_ID = :NEW.USER_ID;
    DBMS_OUTPUT.PUT_LINE('Host ADDED');
END;

CREATE OR REPLACE TRIGGER REMOVE_HOST
AFTER DELETE
ON HOUSES
FOR EACH ROW
DECLARE
	NO_OF_HOUSES NUMBER;
	HID NUMBER := 0;
	PRAGMA AUTONOMOUS_TRANSACTION;
BEGIN
	DBMS_OUTPUT.PUT_LINE('Remove host triggered');
	SELECT COUNT(HOUSE_ID) INTO NO_OF_HOUSES
	FROM HOUSES
	WHERE USER_ID = :OLD.USER_ID;
	
	IF NO_OF_HOUSES = 1 THEN
		SELECT HOUSE_ID INTO HID
		FROM HOUSES
		WHERE USER_ID = :OLD.USER_ID;
	END IF;
	
	IF NO_OF_HOUSES = 1 AND HID = :OLD.HOUSE_ID THEN
		UPDATE USERS
		SET IS_HOST = 0
		WHERE USER_ID = :OLD.USER_ID;
		DBMS_OUTPUT.PUT_LINE('Host removed');
	END IF;
	COMMIT;
END;

ALTER TABLE RENTS
RENAME COLUMN REVIEW
TO HOUSE_RATING;

ALTER TABLE RENTS
RENAME COLUMN REVIEW_COMMENT
TO HOUSE_REVIEW;

ALTER TABLE RENTS
ADD OWNER_RATING NUMBER;

ALTER TABLE RENTS
ADD OWNER_REVIEW VARCHAR2(255);

ALTER TABLE RENTS
ADD REVIEW_DATE DATE;

ALTER TABLE RENTS
ADD RENT_ID NUMBER;

ALTER TABLE RENTS
ADD CONSTRAINT RENT_PK PRIMARY KEY(RENT_ID);

CREATE SEQUENCE S
START WITH     5
INCREMENT BY   1
NOCACHE
NOCYCLE;

ALTER TABLE RENTS
MODIFY RENT_ID DEFAULT S.NEXTVAL;

CREATE OR REPLACE FUNCTION IS_ROOM_AVAILABLE(HID IN NUMBER, RN IN NUMBER, CID IN VARCHAR2, COD IN VARCHAR2, G IN NUMBER)
RETURN CHAR IS
	CNT NUMBER;
	CAPACITY NUMBER;
BEGIN
	SELECT MAX_CAPACITY INTO CAPACITY
	FROM ROOMS
	WHERE HOUSE_ID = HID
	AND ROOM_NO = RN;
	
	IF G <= CAPACITY THEN
		SELECT COUNT(ROOM_NO) INTO CNT
		FROM RENTS
		WHERE HOUSE_ID = HID
		AND ROOM_NO = RN
		AND ((TO_DATE(CID, 'DD-MON-YYYY') BETWEEN CHECKIN AND CHECKOUT)
		OR (TO_DATE(COD, 'DD-MON-YYYY') BETWEEN CHECKIN AND CHECKOUT)
		OR (CHECKIN BETWEEN TO_DATE(CID, 'DD-MON-YYYY') AND TO_DATE(COD, 'DD-MON-YYYY')));
	
		IF CNT = 0 THEN
			RETURN 'Y';
		ELSE
			RETURN 'N';
		END IF;
	END IF;
	RETURN 'N';
END;

--Aungon End--