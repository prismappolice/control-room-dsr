from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import pytz
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

# Indian Standard Time timezone
IST = pytz.timezone('Asia/Kolkata')

def ist_now():
    """Get current time in Indian Standard Time"""
    return datetime.now(IST).replace(tzinfo=None)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)  # 'admin', 'district', 'controlroom'
    district_name = db.Column(db.String(100), nullable=True)  # For district users
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=ist_now)
    last_password_change = db.Column(db.DateTime, default=ist_now)
    
    def set_password(self, password):
        """Set password hash"""
        self.password_hash = generate_password_hash(password)
        self.last_password_change = ist_now()
    
    def check_password(self, password):
        """Check password against hash"""
        return check_password_hash(self.password_hash, password)
    
    # Backward compatibility - support old 'password' attribute
    @property
    def password(self):
        """For backward compatibility, return None since we don't store plain passwords"""
        return None
    
    @password.setter
    def password(self, password):
        """For backward compatibility, set password using hash"""
        self.set_password(password)

class DSREntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    district_name = db.Column(db.String(100), nullable=False)
    form_type = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False)
    data = db.Column(db.Text, nullable=False)  # JSON string of form data
    created_at = db.Column(db.DateTime, default=ist_now)
    updated_at = db.Column(db.DateTime, default=ist_now, onupdate=ist_now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class ControlRoomUpload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    upload_type = db.Column(db.String(50), nullable=False)  # 'periscope', 'vip_engagements', 'ps_rtm', 'next_24hrs_forecast', 'dg_teleconference', 'weekly_dsrs'
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=ist_now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Form configurations
FORM_CONFIGS = {
    'crime_data': {
        'name': 'Crime Data',
        'fields': [
            {'name': 'unit_name', 'type': 'text', 'label': 'Unit Name'},
            {'name': 'crime_head', 'type': 'text', 'label': 'Crime Head'},
            {'name': 'fir_no', 'type': 'text', 'label': 'FIR No'},
            {'name': 'facts_of_case', 'type': 'textarea', 'label': 'Facts of the Case'},
            {'name': 'accused_status', 'type': 'textarea', 'label': 'Accused Status'},
            {'name': 'action_taken', 'type': 'textarea', 'label': 'Action Taken'},
            {'name': 'legal_progress', 'type': 'textarea', 'label': 'Legal Progress'},
            {'name': 'remarks', 'type': 'textarea', 'label': 'Remarks'}
        ]
    },
    'nbw_status': {
        'name': 'Non Bailable Warrants (NBWs) Status',
        'fields': [
            {'name': 'unit_name', 'type': 'text', 'label': 'Unit Name'},
            {'name': 'pending', 'type': 'number', 'label': 'Pending'},
            {'name': 'executed_today', 'type': 'number', 'label': 'Executed Today'},
            {'name': 'one_week_total', 'type': 'number', 'label': '1-Week Total'},
            {'name': 'one_month_total', 'type': 'number', 'label': '1-Month Total'},
            {'name': 'remarks', 'type': 'textarea', 'label': 'Remarks'}
        ]
    },
    'pd_act_proposals': {
        'name': 'PD Act Proposals Monitoring',
        'fields': [
            {'name': 'unit_name', 'type': 'text', 'label': 'Unit Name'},
            {'name': 'case_no', 'type': 'text', 'label': 'Case No'},
            {'name': 'accused_profile', 'type': 'textarea', 'label': 'Accused Profile'},
            {'name': 'crime_type', 'type': 'text', 'label': 'Crime Type'},
            {'name': 'grounds_for_proposal', 'type': 'textarea', 'label': 'Grounds for Proposal'},
            {'name': 'current_status', 'type': 'text', 'label': 'Current Status'},
            {'name': 'remarks', 'type': 'textarea', 'label': 'Remarks'}
        ]
    },
    'externment_actions': {
        'name': 'Externment Actions',
        'fields': [
            {'name': 'unit_name', 'type': 'text', 'label': 'Unit Name'},
            {'name': 'accused_gang', 'type': 'text', 'label': 'Accused/Gang'},
            {'name': 'activity_profile', 'type': 'textarea', 'label': 'Activity Profile'},
            {'name': 'legal_grounds', 'type': 'textarea', 'label': 'Legal Grounds'},
            {'name': 'jurisdiction_ps', 'type': 'text', 'label': 'Jurisdiction PS'},
            {'name': 'status', 'type': 'text', 'label': 'Status'},
            {'name': 'date', 'type': 'date', 'label': 'Date'},
            {'name': 'remarks', 'type': 'textarea', 'label': 'Remarks'}
        ]
    },
    'sensitive_cases': {
        'name': 'Sensitive/Political/High Profile Case Monitoring',
        'fields': [
            {'name': 'unit_name', 'type': 'text', 'label': 'Unit Name'},
            {'name': 'fir_no', 'type': 'text', 'label': 'FIR No'},
            {'name': 'case_category', 'type': 'text', 'label': 'Case Category'},
            {'name': 'crime_head', 'type': 'text', 'label': 'Crime Head'},
            {'name': 'summary', 'type': 'textarea', 'label': 'Summary'},
            {'name': 'todays_progress', 'type': 'textarea', 'label': "Today's Progress"},
            {'name': 'pending_action', 'type': 'textarea', 'label': 'Pending Action'},
            {'name': 'risk_flag', 'type': 'text', 'label': 'Risk Flag'},
            {'name': 'lead_officer', 'type': 'text', 'label': 'Lead Officer'}
        ]
    },
    'vc_productions': {
        'name': 'VC Productions (Under Trials & Remand)',
        'fields': [
            {'name': 'unit_name', 'type': 'text', 'label': 'Unit Name'},
            {'name': 'no_produced', 'type': 'number', 'label': 'No Produced'},
            {'name': 'mode', 'type': 'text', 'label': 'Mode (VC/Physical)'},
            {'name': 'courts_covered', 'type': 'number', 'label': 'Courts Covered'},
            {'name': 'issues_faced', 'type': 'textarea', 'label': 'Issues Faced'},
            {'name': 'mitigation_steps', 'type': 'textarea', 'label': 'Mitigation Steps'}
        ]
    },
    'important_cases': {
        'name': 'Important Cases from Earlier DSRs',
        'fields': [
            {'name': 'unit_name', 'type': 'text', 'label': 'Unit Name'},
            {'name': 'fir_no', 'type': 'text', 'label': 'FIR No'},
            {'name': 'date_added', 'type': 'date', 'label': 'Date Added'},
            {'name': 'todays_progress', 'type': 'textarea', 'label': "Today's Progress"},
            {'name': 'pending_action', 'type': 'textarea', 'label': 'Pending Action'},
            {'name': 'responsible_officer', 'type': 'text', 'label': 'Responsible Officer'},
            {'name': 'next_review_date', 'type': 'date', 'label': 'Next Review Date'}
        ]
    },
    'cctv_surveillance': {
        'name': 'CCTV Surveillance Infrastructure Monitoring',
        'fields': [
            {'name': 'unit_name', 'type': 'text', 'label': 'Unit Name'},
            {'name': 'installed_today', 'type': 'number', 'label': 'Installed Today'},
            {'name': 'total_this_month', 'type': 'number', 'label': 'Total This Month'},
            {'name': 'command_centre_integrated', 'type': 'text', 'label': 'Command Centre Integrated (Y/N)'},
            {'name': 'capabilities', 'type': 'text', 'label': 'Capabilities (ANPR/Night Vision)'},
            {'name': 'maintenance_issues', 'type': 'textarea', 'label': 'Maintenance Issues'}
        ]
    },
    'cyber_crime_monitoring': {
        'name': 'Cyber Crime Monitoring',
        'fields': [
            {'name': 'unit_name', 'type': 'text', 'label': 'Unit Name'},
            {'name': 'complaints_today', 'type': 'number', 'label': 'Complaints Today'},
            {'name': 'firs_registered', 'type': 'number', 'label': 'FIRs Registered'},
            {'name': 'crime_type', 'type': 'text', 'label': 'Crime Type'},
            {'name': 'financial_impact', 'type': 'text', 'label': 'Financial Impact'},
            {'name': 'progress', 'type': 'textarea', 'label': 'Progress'},
            {'name': 'agency_support_required', 'type': 'textarea', 'label': 'Agency Support Required'}
        ]
    },
    'womens_safety': {
        'name': "Women's Safety Monitoring Dashboard",
        'fields': [
            {'name': 'unit_name', 'type': 'text', 'label': 'Unit Name'},
            {'name': 'domestic_violence', 'type': 'number', 'label': 'Domestic Violence'},
            {'name': 'eve_teasing', 'type': 'number', 'label': 'Eve-Teasing'},
            {'name': 'sexual_harassment', 'type': 'number', 'label': 'Sexual Harassment'},
            {'name': 'avg_response_time', 'type': 'text', 'label': 'Avg Response Time'},
            {'name': 'firs', 'type': 'number', 'label': 'FIRs'},
            {'name': 'shakti_team_action', 'type': 'textarea', 'label': 'Shakti Team Action'},
            {'name': 'community_feedback', 'type': 'textarea', 'label': 'Community Feedback'}
        ]
    },
    'focus_area': {
        'name': 'Focus Area of the Day - Command Initiative Tracker',
        'fields': [
            {'name': 'unit_name', 'type': 'text', 'label': 'Unit Name'},
            {'name': 'date', 'type': 'date', 'label': 'Date'},
            {'name': 'theme_problem_area', 'type': 'text', 'label': 'Theme/Problem Area'},
            {'name': 'expected_officer_response', 'type': 'textarea', 'label': 'Expected Officer Response'},
            {'name': 'actual_compliance', 'type': 'textarea', 'label': 'Actual Compliance'},
            {'name': 'gaps_identified', 'type': 'textarea', 'label': 'Gaps Identified'}
        ]
    },
    'legal_monitoring': {
        'name': 'Legal Monitoring Cell',
        'fields': [
            {'name': 'unit_name', 'type': 'text', 'label': 'Unit Name'},
            {'name': 'case_name', 'type': 'text', 'label': 'Case Name'},
            {'name': 'court_bench', 'type': 'text', 'label': 'Court/Bench'},
            {'name': 'next_hearing_date', 'type': 'date', 'label': 'Next Hearing Date'},
            {'name': 'relief_sought', 'type': 'textarea', 'label': 'Relief Sought'},
            {'name': 'police_action_required', 'type': 'textarea', 'label': 'Police Action Required'}
        ]
    },
    'one_page_dsr': {
        'name': 'One Page DSR Summary',
        'fields': [
            {'name': 'unit_name', 'type': 'text', 'label': 'Unit Name'},
            {'name': 'vvip_movements_law_order', 'type': 'textarea', 'label': 'VVIP Movements/Law & Order'},
            {'name': 'crime_important', 'type': 'textarea', 'label': 'Crime (Important)'},
            {'name': 'nbw_pd_externment', 'type': 'textarea', 'label': 'NBW/PD/Externment'},
            {'name': 'cyber_crime', 'type': 'textarea', 'label': 'Cyber Crime'},
            {'name': 'womens_safety', 'type': 'textarea', 'label': "Women's Safety"},
            {'name': 'sensitive_cases', 'type': 'textarea', 'label': 'Sensitive Cases'},
            {'name': 'cctv_surveillance', 'type': 'textarea', 'label': 'CCTV/Surveillance'},
            {'name': 'legal_issues', 'type': 'textarea', 'label': 'Legal Issues'},
            {'name': 'focus_area_progress', 'type': 'textarea', 'label': 'Focus Area Progress'}
        ]
    },
    'cctv_ps_status': {
        'name': 'DSR on Working Status of CCTV Cameras in PS',
        'fields': [
            {'name': 'unit_name', 'type': 'text', 'label': 'Unit Name'},
            {'name': 'no_of_police_stations', 'type': 'number', 'label': 'No of Police Stations'},
            {'name': 'total_cctv_installed', 'type': 'number', 'label': 'Total No of CCTV Cameras Installed'},
            {'name': 'cameras_functioning', 'type': 'number', 'label': 'No of Cameras Functioning'},
            {'name': 'cameras_not_functioning', 'type': 'number', 'label': 'No of Cameras Not Functioning'},
            {'name': 'action_taken_complaints', 'type': 'textarea', 'label': 'Action Taken/No of Complaint Raised'},
            {'name': 'ps_footage_stored', 'type': 'number', 'label': 'In No of PS Footage is being stored'},
            {'name': 'remarks', 'type': 'textarea', 'label': 'Remarks'}
        ]
    },
    'uo_availability': {
        'name': 'Availability of UOs In District HQrs',
        'fields': [
            {'name': 'unit_name', 'type': 'text', 'label': 'Unit Name'},
            {'name': 'remarks', 'type': 'textarea', 'label': 'Remarks'}
        ]
    },
    'cctv_installation_abstract': {
        'name': 'Abstract of Newly Installed CCTV Cameras in Each Unit',
        'fields': [
            {'name': 'unit_name', 'type': 'text', 'label': 'Unit Name'},
            {'name': 'apportioned_target', 'type': 'number', 'label': 'Apportioned Target'},
            {'name': 'cumulative_upto_01_11_2025', 'type': 'number', 'label': 'Cumulative upto/Cameras installed by 01.11.2025'},
            {'name': 'cameras_mapped_gis_02_11_2025', 'type': 'number', 'label': 'How many Cameras mapped on GIS as on 02.11.2025'},
            {'name': 'cameras_installed_02_11_2025', 'type': 'number', 'label': 'Cameras installed on 02.11.2025'},
            {'name': 'cumulative_upto_02_11_2025', 'type': 'number', 'label': 'Cumulative upto 02.11.2025'},
            {'name': 'to_be_completed_31_march_2025', 'type': 'number', 'label': 'To be completed by 31 March 2025'},
            {'name': 'cities_villages_connected', 'type': 'number', 'label': 'Number of cities/villages connected with CCTVs as on 02.11.2025'}
        ]
    },
    'status_ui_cases': {
        'name': 'Status of UI Cases',
        'fields': [
            {'name': 'unit_name', 'type': 'text', 'label': 'Unit Name'},
            {'name': 'total_ui_cases', 'type': 'number', 'label': 'Total no of UI Cases'},
            {'name': 'pending_60_days', 'type': 'number', 'label': 'Pending more than 60 days'},
            {'name': 'pending_90_days', 'type': 'number', 'label': 'Pending more than 90 days'},
            {'name': 'pending_6_months', 'type': 'number', 'label': 'Pending more than 6 months'},
            {'name': 'pending_1_year', 'type': 'number', 'label': 'Pending for above 1 year'},
            {'name': 'action_taken', 'type': 'textarea', 'label': 'Action taken to liquidate pendency and time line'}
        ]
    },
    'status_pt_cases': {
        'name': 'Status of PT Cases',
        'fields': [
            {'name': 'unit_name', 'type': 'text', 'label': 'Unit Name'},
            {'name': 'total_pt_cases', 'type': 'number', 'label': 'Total no of PT Cases'},
            {'name': 'disposed_off', 'type': 'number', 'label': 'Disposed off'},
            {'name': 'convictions', 'type': 'number', 'label': 'Convictions'},
            {'name': 'acquittals', 'type': 'number', 'label': 'Acquittals'},
            {'name': 'conviction_rate', 'type': 'text', 'label': 'Overall Conviction rate (%)'},
            {'name': 'remarks', 'type': 'textarea', 'label': 'Remarks'}
        ]
    },
    'performance_highlights_weekly': {
        'name': 'Dist/UNIT Performance Highlights-Weekly',
        'fields': [
            {'name': 'unit_name', 'type': 'text', 'label': 'Unit name'},
            {'name': 'success_story', 'type': 'textarea', 'label': 'Success story'},
            {'name': 'officers', 'type': 'textarea', 'label': 'Officers(s)'},
            {'name': 'crime_event_type', 'type': 'textarea', 'label': 'Crime/Event type'},
            {'name': 'technique_used', 'type': 'textarea', 'label': 'Technique used'},
            {'name': 'recognition_proposed', 'type': 'textarea', 'label': 'Recognition Proposed'}
        ]
    },
    'weekly_performance_scorecard': {
        'name': 'Weekly Performance Scorecard',
        'fields': [
            {'name': 'unit_name', 'type': 'text', 'label': 'Unit name'},
            {'name': 'crime_detection', 'type': 'textarea', 'label': 'Crime detection'},
            {'name': 'vc_handling', 'type': 'textarea', 'label': 'VC Handling'},
            {'name': 'law_order_response', 'type': 'textarea', 'label': 'Law & Order Response'},
            {'name': 'cyber_womens_cell', 'type': 'textarea', 'label': 'Cyber/women\'s Cell'},
            {'name': 'rating', 'type': 'number', 'label': 'Rating (1-5)'},
            {'name': 'trend_last_week', 'type': 'textarea', 'label': 'Trend Compared to Last Week'}
        ]
    },
    'head_wise_crime_weekly': {
        'name': 'Head Wise Crime Weekly Statement',
        'is_grouped': True,  # Special flag for grouped display
        'fields': [
            {'name': 'unit_head_of_crime', 'type': 'text', 'label': 'Unit/Head of Crime', 'section': None},
            # Bodily Offences Section
            {'name': 'section_bodily', 'type': 'section', 'label': 'Bodily Offences'},
            {'name': 'bodily_murder_gain', 'type': 'text', 'label': 'Murder for gain (302, 379 IPC)', 'section': 'bodily'},
            {'name': 'bodily_murders', 'type': 'text', 'label': 'Murders (302 IPC)', 'section': 'bodily'},
            {'name': 'bodily_attempt_murder', 'type': 'text', 'label': 'Attempt Murder (307 IPC)', 'section': 'bodily'},
            {'name': 'bodily_c_homicides', 'type': 'text', 'label': 'C.Homicides (304 IPC)', 'section': 'bodily'},
            {'name': 'bodily_grave_hurts', 'type': 'text', 'label': 'Grave Hurts (325 & 326 IPC)', 'section': 'bodily'},
            {'name': 'bodily_simple_hurts', 'type': 'text', 'label': 'Simple Hurts (323 & 324 IPC)', 'section': 'bodily'},
            # Property Offences Section
            {'name': 'section_property', 'type': 'section', 'label': 'Property Offences'},
            {'name': 'property_dacoity', 'type': 'text', 'label': 'Dacoity (395 IPC)', 'section': 'property'},
            {'name': 'property_robbery', 'type': 'text', 'label': 'Robbery (392 & 394 IPC)', 'section': 'property'},
            {'name': 'property_hbs_day', 'type': 'text', 'label': 'H.Bs by Day (454, 380 IPC)', 'section': 'property'},
            {'name': 'property_hbs_night', 'type': 'text', 'label': 'H.Bs by Night (457, 380 IPC)', 'section': 'property'},
            {'name': 'property_ordinary_thefts', 'type': 'text', 'label': 'Ordinary Thefts (379, 380 IPC)', 'section': 'property'},
            # Crime Against Women Section
            {'name': 'section_caw', 'type': 'section', 'label': 'Crime Against Women'},
            {'name': 'caw_rape', 'type': 'text', 'label': 'Rape (376 IPC)', 'section': 'caw'},
            {'name': 'caw_others', 'type': 'text', 'label': 'Others (354, 354A, 354D, 509 IPC)', 'section': 'caw'},
            {'name': 'section_pocso', 'type': 'subsection', 'label': 'POCSO', 'parent': 'caw'},
            {'name': 'caw_pocso_sec34_56_grave', 'type': 'text', 'label': 'Sec 3&4/5&6 of POCSO – Grave', 'section': 'pocso'},
            {'name': 'caw_pocso_others_sec12', 'type': 'text', 'label': 'Others (Sec 12) Non-Grave', 'section': 'pocso'},
            {'name': 'caw_dowry_death', 'type': 'text', 'label': 'Dowry Death (304B)', 'section': 'caw'},
            # Other Categories
            {'name': 'sc_st_cases', 'type': 'text', 'label': 'SC-ST Cases'},
            {'name': 'riotings', 'type': 'text', 'label': 'Riotings (147, 148, 149 IPC)'},
            {'name': 'kidnappings', 'type': 'text', 'label': 'Kidnappings (363, 369 IPC)'},
            {'name': 'cheatings', 'type': 'text', 'label': 'Cheatings (420 IPC)'},
            {'name': 'cyber_offences', 'type': 'text', 'label': 'Cyber Offences'},
            # Road Accidents Section
            {'name': 'section_road', 'type': 'section', 'label': 'Road Accidents'},
            {'name': 'road_accidents_fatal', 'type': 'text', 'label': 'Fatal', 'section': 'road'},
            {'name': 'road_accidents_non_fatal', 'type': 'text', 'label': 'Non-Fatal', 'section': 'road'},
            # Final Categories
            {'name': 'other_ipc_stup_drugs', 'type': 'text', 'label': 'Other IPC + Stup. Drugs'},
            {'name': 'sll_cases', 'type': 'text', 'label': 'SLL cases (Excise/AP PROHIBITION Act/Gaming/NDPS/IT Act/etc.)'},
            {'name': 'crpc_174', 'type': 'text', 'label': '174 Cr.P.C'},
            {'name': 'missing_cases', 'type': 'text', 'label': 'Missing Cases'},
            {'name': 'others_if_any', 'type': 'text', 'label': 'Others if any'}
        ]
    }
}

# District names
DISTRICTS = [
    'Srikakulam', 'Vizianagaram', 'Visakhapatnam', 'East Godavari', 'West Godavari',
    'Krishna', 'Guntur', 'Prakasam', 'Nellore', 'Kadapa', 'Kurnool', 'Anantapur',
    'Chittoor', 'Tirupati', 'Nandyal', 'Bapatla', 'Palnadu', 'Eluru', 'Konaseema',
    'Kakinada', 'Anakapalli', 'Alluri Sitarama Raju', 'Parvathipuram Manyam',
    'Annamayya', 'Sri Sathya Sai', 'NTR', 'SRP VJA', 'SRP GTL'
]