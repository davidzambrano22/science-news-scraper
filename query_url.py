"""Search topic in webpage"""

from datetime import datetime
import re

class queryUrl:
    def __init__(self, query, start_date, end_date):
        self.date_correct_pattern = re.compile('\d{2}-\d{2}-\d{4}')
        self.query = query
        self.start_date = start_date
        self.end_date = end_date
    
    def get_url(self):
        try:
            #check if date string is a correct value
            if not re.match(self.date_correct_pattern, self.start_date) and re.match(self.date_correct_pattern, self.end_date):
                raise Exception('Error: Incorrect date format')
            #Check that end_date is not higher than current (today) date
            current_date = datetime.today().strftime('%d-%m-%Y') 
            comparer = compare_date(self.end_date)
            not_exceeds_today = comparer.compare(current_date)
            if not not_exceeds_today:
                raise Exception('Error: Dates must not exceed the current date {}'.format(current_date))
            #Check if start date is older than end date
            comparison = compare_date(self.start_date)
            valid_comparison = comparison.compare(self.end_date)
            if not valid_comparison:
                raise Exception('Error: Start date must be older that end date')
            netloc = 'https://www.sciencenews.org'
            path = '/'
            query_start = '?s='
            words = self.query if len(self.query.split(' ')) == 1 else '+'.join(word for word in self.query.split(' '))
            topic = '&topic='
            start = '&start-date={}'.format(parse_date(self.start_date))
            end = '&end-date={}'.format(parse_date(self.end_date))
            orderby = '&orderby=date'
            url = netloc + path + query_start + words + topic + start + end + orderby
            return url 
        except Exception as e:
            print(e)
            return None

    def urlPlusPage(self, url, page):
        self.path = '/page/{}?s'.format(page)
        self.to_replace = re.compile('/\?s')
        return re.sub(self.to_replace, self.path, url)

#_______________________________________________________________________________________________
"""Compares start date and end date so the first is not more higher than end date"""

class compare_date:
    def __init__(self, start_date):
        self.day, self.month, self.year = start_date.split('-')
    def __repr__(self) -> str:
        return 'Start Date<{}/{}/{}>'.format(self.day, self.month, self.year)

    def compare(self, end_date):
        day, month, year = end_date.split('-')
        if self.year > year:
            return False
        elif self.year <= year:
            if self.month > month and self.year == year:
                return False
            if self.month == month and self.year == year and self.day > day:
                return False
        return True

#___________________________________________________________________________________________
#Parse date
"""Function that parses the input date into a valid format"""

def parse_date(date):
    day, month, year = date.split('-')
    date_template = '{}%2F{}%2F{}'
    return date_template.format(month, day, year)

#___________________________________________________________________________________________

if __name__ == '__main__':
    queryUrl()
        
    