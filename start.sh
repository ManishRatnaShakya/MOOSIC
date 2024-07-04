#!/bin/bash
gunicorn -b 0.0.0.0:$PORT music_recommender:app
