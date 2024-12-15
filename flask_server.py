from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
from phoenix.otel import register
PHOENIX_API_KEY = "ADD YOUR API KEY"
os.environ["PHOENIX_CLIENT_HEADERS"] = f"api_key={PHOENIX_API_KEY}"

# configure the Phoenix tracer
tracer_provider = register(
  project_name="timey", # Default is 'default'
  endpoint="https://app.phoenix.arize.com/v1/traces",
)

app = Flask(__name__)
CORS(app)

nates_calendar = """
[
    {
        "importance": "normal",
        "sensitivity": "normal",
        "isOrganizer": false,
        "webLink": "https://outlook.office365.com/owa/?itemid=AAMkADhhZGYyZjM5LWVlYWEtNDhlMi05MTFkLTU1NTA5NmMxNDYwZgBGAAAAAADiD1ZbMZJtTKq4WZYQEMzwBwBJbFpVNQDSQqGcs867hWEBAAAAABZlAADkpycW1eZhQ70NDlB%2FlVyVAApxgLxvAAA%3D&exvsurl=1&path=/calendar/item",
        "body": {
            "contentType": "html",
            "content": ""
        },
        "start": {
            "dateTime": "2024-12-14T09:00:00"
        },
        "end": {
            "dateTime": "2024-12-14T18:00:00"
        },
        "location": {
            "displayName": "Microsoft Reactor Redmond, 3709 157th Ave NE, Redmond, WA 98052, USA",
            "locationType": "default",
            "uniqueId": "Microsoft Reactor Redmond, 3709 157th Ave NE, Redmond, WA 98052, USA",
            "uniqueIdType": "private"
        },
        "organizer": {
            "emailAddress": {
                "name": "Open Source for AI",
                "address": "calendar-invite@lu.ma"
            }
        },
        "onlineMeeting": null,
        "subject": "Open Source AI Hackathon #12 - AI Agents",
        "bodyPreview": "Open Source for AI"
    },
    {
        "importance": "normal",
        "sensitivity": "normal",
        "isOrganizer": true,
        "webLink": "https://outlook.office365.com/owa/?itemid=AAMkADhhZGYyZjM5LWVlYWEtNDhlMi05MTFkLTU1NTA5NmMxNDYwZgBGAAAAAADiD1ZbMZJtTKq4WZYQEMzwBwBJbFpVNQDSQqGcs867hWEBAAAAABZlAADkpycW1eZhQ70NDlB%2FlVyVAApzCNuTAAA%3D&exvsurl=1&path=/calendar/item",
        "body": {
            "contentType": "html",
            "content": ""
        },
        "start": {
            "dateTime": "2024-12-17T10:00:00"
        },
        "end": {
            "dateTime": "2024-12-17T11:00:00"
        },
        "location": {
            "displayName": "",
            "locationType": "default",
            "uniqueIdType": "unknown",
            "address": {},
            "coordinates": {}
        },
        "organizer": {
            "emailAddress": {
                "name": "Nate W",
                "address": "nate@whatever.net"
            }
        },
        "onlineMeeting": null,
        "subject": "Phone call about national AI policy",
        "bodyPreview": ""
    },
    {
        "importance": "normal",
        "sensitivity": "normal",
        "isOrganizer": true,
        "webLink": "https://outlook.office365.com/owa/?itemid=AAMkADhhZGYyZjM5LWVlYWEtNDhlMi05MTFkLTU1NTA5NmMxNDYwZgBGAAAAAADiD1ZbMZJtTKq4WZYQEMzwBwBJbFpVNQDSQqGcs867hWEBAAAAABZlAADkpycW1eZhQ70NDlB%2FlVyVAApzCNuSAAA%3D&exvsurl=1&path=/calendar/item",
        "body": {
            "contentType": "html",
            "content": ""
        },
        "start": {
            "dateTime": "2024-12-17T13:00:00"
        },
        "end": {
            "dateTime": "2024-12-17T14:00:00"
        },
        "location": {
            "displayName": "Microsoft Reactor Redmond",
            "locationUri": "https://www.bingapis.com/api/v6/localbusinesses/YN873x18209996613658749749",
            "locationType": "localBusiness",
            "uniqueId": "https://www.bingapis.com/api/v6/localbusinesses/YN873x18209996613658749749",
            "uniqueIdType": "bing",
            "address": {
                "street": "3709 157th Ave NE",
                "city": "Redmond",
                "state": "WA",
                "countryOrRegion": "United States",
                "postalCode": ""
            },
            "coordinates": {
                "latitude": 47.6437,
                "longitude": -122.131
            }
        },
        "organizer": {
            "emailAddress": {
                "name": "Nate W",
                "address": "nate@whatever.net"
            }
        },
        "onlineMeeting": null,
        "subject": "Review AI policy with the team",
        "bodyPreview": ""
    },
    {
        "importance": "normal",
        "sensitivity": "normal",
        "isOrganizer": true,
        "webLink": "https://outlook.office365.com/owa/?itemid=AAMkADhhZGYyZjM5LWVlYWEtNDhlMi05MTFkLTU1NTA5NmMxNDYwZgBGAAAAAADiD1ZbMZJtTKq4WZYQEMzwBwBJbFpVNQDSQqGcs867hWEBAAAAABZlAADkpycW1eZhQ70NDlB%2FlVyVAApzCNuRAAA%3D&exvsurl=1&path=/calendar/item",
        "body": {
            "contentType": "html",
            "content": "White House"
        },
        "start": {
            "dateTime": "2024-12-25T12:00:00"
        },
        "end": {
            "dateTime": "2024-12-25T13:00:00"
        },
        "location": {
            "displayName": "",
            "locationType": "default",
            "uniqueIdType": "unknown",
            "address": {},
            "coordinates": {}
        },
        "organizer": {
            "emailAddress": {
                "name": "Nate W",
                "address": "nate@whatever.net"
            }
        },
        "onlineMeeting": null,
        "subject": "Present our AI policy to the president.",
        "bodyPreview": "White House"
    },
    {
        "importance": "normal",
        "sensitivity": "private",
        "isOrganizer": true,
        "webLink": "https://outlook.office365.com/owa/?itemid=AAMkADhhZGYyZjM5LWVlYWEtNDhlMi05MTFkLTU1NTA5NmMxNDYwZgFRAAgI3R%2FAFNKAAEYAAAAA4g9WWzGSbUyquFmWEBDM8AcASWxaVTUA0kKhnLPOu4VhAQAAAAAWZQAA5KcnFtXmYUO9DQ5Qf5VclQAA9xPdgwAAEA%3D%3D&exvsurl=1&path=/calendar/item",
        "body": {
            "contentType": "html",
            "content": "Microsoft Exchange Server"
        },
        "start": {
            "dateTime": "2024-12-19T21:00:00"
        },
        "end": {
            "dateTime": "2024-12-19T22:00:00"
        },
        "location": {
            "displayName": "",
            "locationType": "default",
            "uniqueIdType": "unknown",
            "address": {},
            "coordinates": {}
        },
        "organizer": {
            "emailAddress": {
                "name": "Nate W",
                "address": "nate@whatever.net"
            }
        },
        "onlineMeeting": null,
        "subject": "Take out trash cans.",
        "bodyPreview": ""
    }
]
"""

client = openai.OpenAI(
    api_key=os.environ.get('OPEN_API_KEY'),
)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get("message", "")
    
    prompt = """
        Objective:
        hey, You are an executive assistant that is focussed on organizing Nate's life. 
        Your objective is look into Nate's calendar json and respond to the message in output section of this prompt.
        You will be have Nate's calendar events in JSON format. The calendar events is future looking and can be for the next few months.
        As you may know, some meetings require preparation. For instance, may be Nate needs to prepare presentations ahead or talk to other people to get information, or do research about it, etc.
        Other events can be reminded on the day. 
        You can make this determinate based on the event's title, location, organizers, participants or other information you may find relevant.
        Do not remind about events that are not important for the day.

        Output:
        {user_message}

        Nate's specifics:
        - Below you can find nate's hotmail calendar events for the next week in json. 
        - Nate is in PST timezone. 
        - Current PST time is Sat Dec 14. 

        Your behavior:
        You are personal assistant. Use friendly today and address Nate directly. Address this in like an text message format.

        JSON:  
    """.format(user_message=user_message)

    print(prompt)

    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    try:
        response = client.chat.completions.create(
            messages=[
                    {
                        "role": "user",
                        "content": prompt + nates_calendar
                    }
                ],
                model="gpt-4o",
        )
        print("abc123")
        print(response)

        ai_response = response.choices[0].message.content
        return jsonify({"response": ai_response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
