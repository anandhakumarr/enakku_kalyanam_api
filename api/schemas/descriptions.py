desc_source_name = """

If empty string - empty result

If empty list - all entries

List with only empty string(s) - empty result

Else as per the filter value specified

"""

desc_process_source = """

Source of type ‘Process’ would only be allowed.
‘Datasource’ type - Deprecated - would be removed in future. 

"""

desc_data_source = """

Source of type ‘Data’ is only allowed.

"""

desc_source_isactive = """

Default value: True

"""

desc_source_numPrevDays = """

Default value: 1

"""

desc_line_braak = """
****
"""

desc_required_admin = """

Restricted only to admin users

****

"""


desc_required_maintainer = """

Restricted only to Maintainers

****

"""


desc_slack_channels = """

Value will be overwritten.
For updates, fetch old value and append desired value in input

"""

desc_source_dashtrigger = """

Applicable only for Dashboard type source

"""


desc_source_dashtrigger_validation = """

Dash trigger id is only Applicable for Dashboard type source

"""


desc_startlogdate = """

Only startLogdate specified but no endLogdate : all entries with logdate >= startLogdate

startLogdate = endLogdate : only for specific logdate 

startLogdate > endLogdate : error

"""

desc_endlogdate = """

Only endLogdate specified but no startlogdate - all entries with logdate <= startlogdate

startlogdate = endLogdate : only for specific logdate 

startlogdate > endLogdate : error

"""

desc_history = "History field contains a list of entries from corresponding history table for the particular result entry"


desc_date = """

Input is accepted in date format (yyyy-mm-dd)

"""

desc_status = """

Result is as per the filter value specified

"""

desc_failure_reason = """

Result is as per the filter value specified

"""


desc_isoptional = """

True - returns all entries with value True

False - returns all entries with value false or no value

"""

desc_size = """

Number of elemnts to return per page ( default : 100)

"""

desc_page = """

To filter paginated data ( default : 1)

"""


desc_wrapper = """

The default number of entries in response is 100.
The results are in descending order of logdate in the response.

"""