import pyodbc 
import pandas as pd


"""
Install FreeTDS and unixODBC
The connection to SQL Server will be made using the unixODBC driver manager and the FreeTDS driver. Installing them is most easily done using homebrew, the Mac package manager:

brew update
brew install unixodbc freetds
pip install pyodbc

Connecting without modifying odbcinst.ini or odbc.ini
If you want to avoid modifying both odbc.ini and odbcinst.ini, you can just specify the driver file location in the driver param in pyodbc.connect.

E.g.:

cnx = pyodbc.connect(
    server="my-server.com",
    database="mydb",
    user='myuser',
    tds_version='7.4',
    password="mypassword",
    port=1433,
    driver='/usr/local/lib/libtdsodbc.so')
    
"""

def get_data():
    
    conn = pyodbc.connect(server="178.157.9.109",
                      database="GIMAS",
                      user='sa', 
                      tds_version='7.4', 
                      password="LOGO1!", 
                      port=1433, 
                      driver='/usr/local/lib/libtdsodbc.so'
                      )
    
    nakit_akis_detayli_query = pd.read_sql_query(
  
    '''
    SELECT "Firma"='022', "Donem"='01',
    'Gelir' COLLATE database_default  AS "GelirGider",
    'Kasa' COLLATE database_default AS "Grup",
    CONVERT(VARCHAR, KSCARD.CODE)+' '+KSCARD.NAME COLLATE database_default as "HesapAdi",
    "Yil"=DATEPART(YEAR, GETDATE()-1),
    "AyNo"=DATEPART(MONTH, GETDATE()-1),
    DATEPART(week, GETDATE()-1) AS "Hafta", 
    CONVERT(DATETIME, convert(VARCHAR, (GETDATE()-1), 112)) AS "Vade",
    convert(DECIMAL(18,2), AMOUNT)*(CASE WHEN KSLINES.SIGN=0 THEN 1 ELSE -1 END) AS "Tutar",
    CONVERT(VARCHAR, KSLINES.DATE_, 104) COLLATE database_default AS "Aciklama1",
    TRCODES.CashTrCode COLLATE database_default AS "Aciklama2"
    FROM LG_022_01_KSLINES KSLINES
    INNER JOIN LG_022_KSCARD KSCARD ON KSLINES.CARDREF=KSCARD.LOGICALREF
    LEFT JOIN QS_CASHTRCODES TRCODES ON TRCODES.CashTrCodeType=KSLINES.TRCODE
    WHERE KSLINES.DATE_<=GETDATE()

    UNION ALL

    SELECT "Firma"='022', "Donem"='01',
    'Gelir' COLLATE database_default AS "GelirGider",
    'Banka' COLLATE database_default AS "Grup",
    CONVERT(VARCHAR, BankaCC.CODE)+' '+BankaCC.DEFINITION_ COLLATE database_default as "HesapAdi",
    "Yil"=DATEPART(YEAR, GETDATE()-1),
    "AyNo"=DATEPART(MONTH, GETDATE()-1),
    DATEPART(week, GETDATE()-1) AS "Hafta", 
    CONVERT(DATETIME, convert(VARCHAR, (GETDATE()-1), 112)) AS "Vade",
    convert(DECIMAL(18,2), AMOUNT)*(CASE WHEN BNFLINE.SIGN=0 THEN 1 ELSE -1 END) AS "Tutar",
    CONVERT(VARCHAR, BNFLINE.DATE_, 104) COLLATE database_default AS "Aciklama1",
    CASE BNFLINE.TRCODE 
    WHEN 1 THEN 'Banka Islem Fisi' 
    WHEN 2 THEN 'Banka Virman Fisi' 
    WHEN 3 THEN 'Gelen Havale / EFT' 
    WHEN 4 THEN 'Gonderilen Havale / EFT'
    WHEN 5 THEN 'Banka Acilis Fisi'
    WHEN 10 THEN 'Cek Cikis (Banka Tahsil)'
    ELSE 'Tanimsiz' END COLLATE database_default AS "Aciklama2"
    FROM LG_022_01_BNFLINE BNFLINE
    INNER JOIN LG_022_BankaCC BankaCC ON BNFLINE.BNACCREF=BankaCC.LOGICALREF
    WHERE AMOUNT<>0
    AND BNFLINE.DATE_<GETDATE()
    UNION 
    SELECT "Firma"='022', "Donem"='01',
    case WHEN CSCARD.CURRSTAT IN (9,10) THEN 'Gider' ELSE 'Gelir' END COLLATE database_default AS "GelirGider",
    CASE WHEN CSCARD.DOC=1 AND CSCARD.CURRSTAT=1 THEN 'Portfoydeki Cekler'
    WHEN CSCARD.DOC=1 AND CSCARD.CURRSTAT=4 THEN 'Tahsildeki Cekler'
    WHEN CSCARD.DOC=3 AND CSCARD.CURRSTAT=9 THEN 'Kesilen Cekler'
    WHEN CSCARD.DOC=2 AND CSCARD.CURRSTAT=1 THEN 'Portfoydeki Senetler' 
    WHEN CSCARD.DOC=2 AND CSCARD.CURRSTAT=5 THEN 'Tahsildeki Senetler' 
    WHEN CSCARD.DOC=4 AND CSCARD.CURRSTAT=10 THEN 'Kesilen Senetler' 
    end COLLATE database_default AS "Grup",
    CASE CSCARD.CURRSTAT WHEN 1 THEN CONVERT(VARCHAR, CLCARD.CODE)+' '+CLCARD.DEFINITION_
    WHEN 4 THEN CONVERT(VARCHAR, BankaCC.CODE)+' '+BankaCC.DEFINITION_ 
    WHEN 9 THEN CONVERT(VARCHAR, OURBANK.CODE)+' '+OURBANK.DEFINITION_ 
    END COLLATE database_default as "HesapAdi",
    "Yil"=DATEPART(YEAR, CSCARD.DUEDATE),
    "AyNo"=DATEPART(MONTH, CSCARD.DUEDATE),
    DATEPART(week, CSCARD.DUEDATE) AS "Hafta",
    CSCARD.DUEDATE AS "Vade",
    CAST((CASE WHEN CSCARD.CURRSTAT IN(9,10) THEN (AMOUNT)*-1 ELSE AMOUNT END) AS DECIMAL(18,2)) AS "Tutar",
    PORTFOYNO COLLATE database_default AS "Aciklama1",
    (SELECT CLCARD.CODE +' '+CLCARD.DEFINITION_
    FROM LG_022_CLCARD CLCARD
    WHERE LOGICALREF=
    (SELECT CARDREF
    FROM LG_022_01_CSTRANS CST
    WHERE CST.CSREF=CSCARD.LOGICALREF
    AND STATNO=
    (SELECT MAX(STATNO) 
    FROM LG_022_01_CSTRANS CSTR
    WHERE CST.CSREF=CSTR.CSREF AND CSTR.STATUS=1))) COLLATE database_default AS "Aciklama2"
    FROM LG_022_01_CSCARD CSCARD
    INNER JOIN LG_022_01_CSTRANS CSTRANS ON CSTRANS.CSREF=CSCARD.LOGICALREF AND CSTRANS.STATNO=1
    LEFT JOIN LG_022_01_CSROLL CSROLL ON CSROLL.LOGICALREF=CSTRANS.ROLLREF
    LEFT JOIN LG_022_CLCARD CLCARD ON CLCARD.LOGICALREF=CSTRANS.CARDREF AND CSCARD.CURRSTAT=1
    LEFT JOIN LG_022_BankaCC BankaCC ON BankaCC.LOGICALREF=CSTRANS.CARDREF AND CSCARD.CURRSTAT IN (4)
    LEFT JOIN LG_022_BankaCC OURBANK ON OURBANK.LOGICALREF=CSCARD.OURBANKREF AND CSCARD.CURRSTAT IN (9)
    where (doc IN (1,3) and CURRSTAT IN (1, 4, 9))
    or (DOC IN(2,4) AND CURRSTAT IN (1, 5, 10))
    UNION


    SELECT 
    "Firma"='022', "Donem"='01',
    'Gelir' COLLATE database_default AS "GelirGider",
    'Borclu Cariler' COLLATE database_default AS "Grup",
    CONVERT(VARCHAR, CLCARD.CODE)+' '+CLCARD.DEFINITION_ COLLATE database_default as "HesapAdi",
    "Yil"=DATEPART(YEAR, case when DATE_<=getdate() THEN GETDATE() ELSE PAYTRANS.DATE_ END),
    "AyNo"=DATEPART(MONTH, case when DATE_<=getdate() THEN GETDATE() ELSE PAYTRANS.DATE_ END),
    DATEPART(week, case when DATE_<=getdate() THEN GETDATE() ELSE PAYTRANS.DATE_ END) AS "Hafta",
    case when DATE_<=getdate() THEN CONVERT(DATETIME, convert(VARCHAR, (GETDATE()-1), 112)) ELSE PAYTRANS.DATE_ END AS "Vade",
    CAST(SUM(CASE WHEN SIGN=1 THEN (TOTAL-PAID)*-1 ELSE TOTAL-PAID END) AS DECIMAL(18,2)) AS "Tutar",
    NULL AS "Aciklama1",
    NULL AS "Aciklama2"
    FROM QS_STD_T_1_022_01_CARIRAPOR PAYTRANS
    INNER JOIN LG_022_CLCARD CLCARD ON CLCARD.LOGICALREF=PAYTRANS.CARDREF
    WHERE CROSSREF=0
    AND CARDREF IN (SELECT CARDREF FROM QS_STD_T_1_022_01_CARIRAPOR GROUP BY CARDREF HAVING SUM(KALAN)>0)
    GROUP BY CLCARD.CODE, CLCARD.deFINITION_,PAYTRANS.DATE_

    UNION ALL
    SELECT 
    "Firma"='022', "Donem"='01',
    'Gider' AS "GelirGider",
    'Alacakli Cariler' AS "Grup",
    CONVERT(VARCHAR, CLCARD.CODE)+' '+CLCARD.DEFINITION_ as "HesapAdi",
    "Yil"=DATEPART(YEAR, case when DATE_<=getdate() THEN GETDATE() ELSE PAYTRANS.DATE_ END),
    "AyNo"=DATEPART(MONTH, case when DATE_<=getdate() THEN GETDATE() ELSE PAYTRANS.DATE_ END),
    DATEPART(week, case when DATE_<=getdate() THEN GETDATE() ELSE PAYTRANS.DATE_ END) AS "Hafta",
    case when DATE_<=getdate() THEN CONVERT(DATETIME, convert(VARCHAR, (GETDATE() - 1), 112)) ELSE PAYTRANS.DATE_ END AS "Vade",
    CAST(SUM(CASE WHEN SIGN=1 THEN (TOTAL-PAID)*-1 ELSE TOTAL-PAID END) AS DECIMAL(18,2))*-1 AS "Tutar",
    NULL AS "Aciklama1",
    NULL AS "Aciklama2"
    FROM QS_STD_T_1_022_01_CARIRAPOR PAYTRANS
    INNER JOIN LG_022_CLCARD CLCARD ON CLCARD.LOGICALREF=PAYTRANS.CARDREF
    WHERE PAYTRANS.CROSSREF=0
    AND CARDREF IN (SELECT CARDREF FROM QS_STD_T_1_022_01_CARIRAPOR GROUP BY CARDREF HAVING SUM(KALAN)<0)
    GROUP BY CLCARD.CODE, CLCARD.DEFINITION_, PAYTRANS.DATE_
        
        
        ''', conn)
    
    df = pd.DataFrame(nakit_akis_detayli_query)
    return df


# df = get_data()
# print(df.head())