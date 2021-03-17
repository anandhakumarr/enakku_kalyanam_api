from graphql import GraphQLError
from api.models import *


class Validation:

    def validate_process_source(source):
        if Source.objects.filter(source=source).exclude(type__in=["Datasource", "Process"]):
            raise GraphQLError("Invalid Source Type, Please contact support.")
        return Source.objects.get(source=source)

    def validate_source_type(source_type):
        if source_type not in [ t.type for t in SourceType.objects.all()]:
            raise GraphQLError("Invalid Source Type, Please contact support.")

    def validate_sourcemap_sourcetype(source):
        if Source.objects.filter(source=source).exclude(type__in=[ t.type for t in SourceType.objects.filter(isgroup=True, isactive=True)]):
            raise GraphQLError("Invalid Source Type, Please contact support.")
        source = Source.objects.filter(source=source).first()
        if source:
            return source
        else:
            raise GraphQLError("Source matching query does not exist.")

    def validate_sourcemap_childsourcetype(source):
        if Source.objects.filter(source=source).exclude(type__in=[ t.type for t in SourceType.objects.filter(isactive=True)]):
            raise GraphQLError("Invalid Child Source Type, Please contact support.")
        source = Source.objects.filter(source=source).first()
        if source:
            return source
        else:
            raise GraphQLError("Child Source matching query does not exist.")

    def validate_process_status(status):
        if status.upper() not in ProcessStatusList:
            raise GraphQLError("Invalid status type, Please contact support.")
        return status.upper()

    def validate_data_source(source):
        if Source.objects.filter(source=source).exclude(type__in=["Data"]):
            raise GraphQLError("Invalid Source Type, Please contact support.")
        return source

    def validate_data_status(status):
        if not DataStatusLookup.objects.get(status=status):
            raise GraphQLError("Invalid status type, Please contact support.")
        return status

    def validate_alert_level(alert_level):
        res =  SlackAlertLevel.objects.filter(alert_level=alert_level).first()
        if not res:
            raise GraphQLError("Invalid Alert Level, Please contact support.")
        return res
    
    def validate_alert_source(source):
        if not Source.objects.filter(source=source):
            raise GraphQLError("Invalid Source")
        return source

    def check_is_list_empty(value, field):
        if value is None or value==[] or len(value) == 0 or value == ['']:
            raise GraphQLError("{0} field can't be empty".format(field.title()))

    def check_is_date_empty(value, field):
        if value is None or value=='':
            raise GraphQLError("{0} field can't be empty".format(field.title()))

    def check_is_empty(value, field):
        if value is None or value=='' or value.isspace():
            raise GraphQLError("{0} field can't be empty".format(field.title()))

    def validate_maintenance_status(status):
        if status not in ['Completed On Time', 'Delayed', 'Failed']:
            raise GraphQLError("Invalid Status value, Please contact support.")

    def validate_logdate_window(logdate_window):
        if logdate_window not in ['Daily', 'Daily + previous day', 'Weekly', 'Monthly']:
            raise GraphQLError("Invalid Logdate Window, Please contact Support.")

    def validate_dashboard_title(dashboard_title):
        if dashboard_title.lower().strip() == 'default':
            raise GraphQLError("Default dashboard title is not allowed, Please contact Support.")
