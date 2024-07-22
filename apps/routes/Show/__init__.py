from flask import Blueprint, render_template, request, redirect, url_for, session, make_response, flash, current_app as app
from datetime import datetime

# from .... import TITLE_DASHBD
from ..utilities import *

import requests, json


show = Blueprint(
    name='show',
    import_name=__name__,
    url_prefix='/',
    template_folder="../../templates/layouts/invitation"
)


@show.get('show/')
def show_template():
    data = dict()
    data['template'] = get_detail_template()
    print(data['template'])
    dt = datetime.now()

    if data['template']['category'].upper() == "PERNIKAHAN": 
        data['invitation'] = {
            "category": "Pernikahan",
            "category_id": 1,
            "detail_info": {
                "location": "Hotel ABC, Kota A",
                "maps": "https://maps.app.goo.gl/",
                "marriage_date": "01 January 2024",
                "marriage_end": {
                    "date": "01 Jan 2024",
                    "date_time": "01 Jan 2024 09:00 AM",
                    "dates": "01",
                    "day": "Senin",
                    "day_month": "01 Jan",
                    "edate_time": "01 January 2024 09:00 AM",
                    "etime": "09:00 AM",
                    "full": "Senin, 01 Jan 2024, 09:00:00",
                    "fullmonth": "Januari",
                    "hour": "09",
                    "minute": "00",
                    "month": "Jan",
                    "month_year": "Jan 2024",
                    "no_month": "01",
                    "time": "09:00",
                    "year": "2024"
                },
                "marriage_start": {
                    "date": "01 Jan 2024",
                    "date_time": "01 Jan 2024 08:00 AM",
                    "dates": "01",
                    "day": "Senin",
                    "day_month": "01 Jan",
                    "edate_time": "01 January 2024 08:00 AM",
                    "etime": "08:00 AM",
                    "full": "Senin, 01 Jan 2024, 08:00:00",
                    "fullmonth": "Januari",
                    "hour": "08",
                    "minute": "00",
                    "month": "Jan",
                    "month_year": "Jan 2024",
                    "no_month": "01",
                    "time": "08:00",
                    "year": "2024"
                },
                "reception_date": "30 July 2024",
                "reception_end": {
                    "date": "02 Jan 2024",
                    "date_time": "02 Jan 2024 07:00 PM",
                    "dates": "02",
                    "day": "Selasa",
                    "day_month": "02 Jan",
                    "edate_time": "02 January 2024 07:00 PM",
                    "etime": "07:00 PM",
                    "full": "Selasa, 07 Jan 2024, 19:00:00",
                    "fullmonth": "Januari",
                    "hour": "19",
                    "minute": "00",
                    "month": "Jan",
                    "month_year": "Jan 2024",
                    "no_month": "01",
                    "time": "19:00",
                    "year": "2024"
                },
                "reception_start": {
                    "date": "02 Jan 2024",
                    "date_time": "02 Jan 2024 07:00 AM",
                    "dates": "02",
                    "day": "Selasa",
                    "day_month": "02 Jan",
                    "edate_time": "02 January 2024 07:00 AM",
                    "etime": "07:00 AM",
                    "full": "Selasa, 02 Jan 2024, 07:00:00",
                    "fullmonth": "Januari",
                    "hour": "07",
                    "minute": "00",
                    "month": "Jan",
                    "month_year": "Jan 2024",
                    "no_month": "01",
                    "time": "07:00",
                    "year": "2024"
                }
            },
            "invitation_code": "xxxxxx",
            "invitation_id": 1,
            "invitation_link": "xxxxxx",
            "invitation_title": "Template Pernikahan",
            "personal_data": {
                "man_fullname": "Nama Lengkap Mempelai Pria",
                "man_name": "Pria",
                "mans_photo": "http://127.0.0.1:5000/invitation/media/2024-07-21_043130_QzXuiE_man_photo_5.jpg",
                "son_no": "1",
                "man_dad_status": "0",
                "mans_dad": "Nama Ayah Mempelai Pria",
                "man_mom_status": "0",
                "mans_mom": "Nama Ibu Mempelai Pria",
                "man_address": "Desa asal Mempelai pria",
                "mp_filename": "2024-07-21_043130_QzXuiE_man_photo_5.jpg",
                
                "woman_fullname": "Nama Lengkap Mempelai Wanita",
                "woman_name": "Wanita",
                "womans_photo": "http://127.0.0.1:5000/invitation/media/2024-07-21_044419_QzXuiE_woman_photo_5.jpg",
                "daughter_no": "1",
                "woman_dad_status": "Alm",
                "womans_dad": "Nama Ayah Mempelai Wanita",
                "woman_mom_status": "Almh",
                "womans_mom": "Nama Ibu Mempelai Wanita",
                "woman_address": "Desa asal Mempelai Wanita",
                "wp_filename": "2024-07-21_044419_QzXuiE_woman_photo_5.jpg"
            },
            "template_css": data['template']['css_file'],
            "template_id": 14,
            "template_js": data['template']['js_file'],
            "template_thumb": data['template']['thumbnail'],
            "template_title": "Sepia Floral Orange",
            "template_wall": data['template']['wallpaper'],
            "template_wall2": data['template']['wallpaper_2'],
            "user_id": 5
        }
        wall1_url = data['invitation']['template_wall']
        wall2_url = data['invitation']['template_wall2']
        return render_template(
            title=data['template']['title'],
            data=data,
            background1_url= wall1_url,
            background2_url= wall2_url,
            template_name_or_list='base_wedding.html'
        )
    
    if data['template']['category'].upper() == "ULANG TAHUN": 
        data['invitation'] = {
            "category": "Pernikahan",
            "category_id": 1,
            "detail_info": {
                "date": "01 January 2024",
                "start": {
                    "date": "01 Jan 2024",
                    "date_time": "01 Jan 2024 07:00 AM",
                    "dates": "01",
                    "day": "Senin",
                    "day_month": "01 Jan",
                    "edate_time": "01 January 2024 07:00 AM",
                    "etime": "07:00 AM",
                    "full": "Senin, 01 Jan 2024, 07:00:00",
                    "fullmonth": "Januari",
                    "hour": "07",
                    "minute": "00",
                    "month": "Jan",
                    "month_year": "Jan 2024",
                    "no_month": "01",
                    "time": "07:00",
                    "year": "2024"
                },
                "end": {
                    "date": "01 Jan 2024",
                    "date_time": "01 Jan 2024 10:00 AM",
                    "dates": "01",
                    "day": "Senin",
                    "day_month": "01 Jan",
                    "edate_time": "01 January 2024 10:00 AM",
                    "etime": "10:00 AM",
                    "full": "Senin, 01 Jan 2024, 10:00:00",
                    "fullmonth": "Januari",
                    "hour": "10",
                    "minute": "00",
                    "month": "Jan",
                    "month_year": "Jan 2024",
                    "no_month": "01",
                    "time": "07:00",
                    "year": "2024"
                },
                "dresscode": "White & Cream",
                "location": "Hotel ABC, Kota A",
                "maps": "https://maps.app.goo.gl/",
            },
            "invitation_code": "xxxxxx",
            "invitation_id": 1,
            "invitation_link": "xxxxxx",
            "invitation_title": "Template Ulang Tahun",
            "personal_data": {
                "fullname": "Nama Lengkap",
                "callname": "Nama",
                "myphoto": "http://127.0.0.1:5000/invitation/media/2024-07-21_043130_QzXuiE_man_photo_5.jpg",
                "birthday": "17",
            },
            "template_css": data['template']['css_file'],
            "template_id": 14,
            "template_js": data['template']['js_file'],
            "template_thumb": data['template']['thumbnail'],
            "template_title": "Sepia Floral Orange",
            "template_wall": data['template']['wallpaper'],
            "template_wall2": data['template']['wallpaper_2'],
            "user_id": 5
        }
        wall1_url = data['invitation']['template_wall']
        wall2_url = data['invitation']['template_wall2']
        return render_template(
            title=data['template']['title'],
            data=data,
            background1_url= wall1_url,
            background2_url= wall2_url,
            template_name_or_list='base_birthday.html'
        )


@show.get('<code>/<title>')
def show_invitation(code, title):
    data = dict()
    data['invitation'] = get_detail_code_invitation(code) # code
    # data['template'] = get_detail_template()
    # data['guest'] = get_detail_guest()
    invTitle = data['invitation']['invitation_title']
    wall1_url = data['invitation']['template_wall']
    wall2_url = data['invitation']['template_wall2']

    if data['invitation']['category'].upper() == "PERNIKAHAN":
        return render_template(
            title=invTitle,
            data = data,
            background1_url= wall1_url,
            background2_url= wall2_url,
            template_name_or_list='base_wedding.html'
        )
    elif data['invitation']['category'].upper() == "ULANG TAHUN":
        return render_template(
            title=invTitle,
            data = data,
            background1_url= wall1_url,
            background2_url= wall2_url,
            template_name_or_list='base_birthday.html'
        )

