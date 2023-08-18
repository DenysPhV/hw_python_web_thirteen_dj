from datetime import datetime

import json
from models import Tag, Author, Quote


def fill_db():
    with open('static/hw_ten_app/authors.json', 'r', encoding='utf-8') as fh:
        results = json.load(fh)
        for result in results:
            new_author = Author(description=result['description'],
                                born_date=datetime.strptime(result['born_date'], '%B %d, %Y').date(),
                                born_location=result['born_location'],
                                fullname=result['fullname']
                                )
            new_author.save()


fill_db()
