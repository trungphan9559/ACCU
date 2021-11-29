
GET_TIME_AVG_TIME_CUT_OFF = """
select GROUPS,Province,District,NE_type,network,vendor,NE,SITE,SDATE,EDATE,Round((EDATE-SDATE)*1440,2) Duration,alarm_type,alarm_name,alarm_info from soca.R_alarm_log
where SDATE >= to_date ('11-11-2021','DD-MM-YYYY')
and alarm_type = 'POWER' and region = 'MT' and Round((EDATE-SDATE)*1440,2) >= 15 """


GET_TIME_BACKUP_ACCU = """
SELECT SYSDATE as DATETIME, SITE_ID, to_date(SDATE, 'DD-MM-YYYY HH24:MI:SS') BAT_DAU, to_date(EDATE, 'DD-MM-YYYY HH24:MI:SS') KET_THUC,Round((EDATE-SDATE)*1440,2) Thoi_gian_MLL,ALARM_NAME,
PROVINCE, DISTRICT, MA_PHONG_XL, NETWORK, NN_CAP_1,NN_CAP_2, NN_CAP_3, MD_SDATE Thoi_gian_mat_dien, Round((SDATE-MD_SDATE)*1440,2) Thoi_gian_chay_Accu,region  TTML
FROM soca.R_ALARM_SITE_MLL
where SDATE >= to_date ('01-11-2021','DD-MM-YYYY')
AND NN_CAP_1='Nguồn' and region = 'MT' and MD_Sdate is not null
"""





# select DISTRICT,PROVINCE,GROUPS,NETWORK,VENDOR,NE,SITE,SDATE,EDATE,ALARM_TYPE,ALARM_NAME,ALARM_INFO from soca.r_alarm_log
# where (Sdate >= to_date('01-11-2021','dd-mm-yyyy') and region = 'MT' and ALARM_NAME like '%Battery-Deep-Discharge%') or
# (Sdate >= to_date('01-11-2021','dd-mm-yyyy') and region = 'MT' and ALARM_INFO like '%Low battery Alarm%')or
# (Sdate >= to_date('01-11-2021','dd-mm-yyyy') and region = 'MT' and ALARM_TYPE = 'POWER') FETCH FIRST 5 ROWS ONLY






