from flask import Flask, request, jsonify
from concurrent.futures import ThreadPoolExecutor
import time

from .main import run_main
from .check_tourney_time import check_tourney_time_interface

app = Flask(__name__)

# Create a thread pool to handle background tasks
executor = ThreadPoolExecutor(max_workers=5)

@app.route('/check-tournaments', methods=['GET'])
def run_check_tournaments():
    check_tourney_time_interface()
    return jsonify({"message": "Check Tournaments done!"})

def run_full_scraper(task_id):
    print(f"[{task_id}] Starting Scraper")
    run_main()
    print(f"[{task_id}] Scraper finished.")

@app.route('/start-full-scraper', methods=['GET'])
def start_full_scraper():
    task_id = request.args.get("task_id", "default")
    executor.submit(run_full_scraper, task_id)
    return jsonify({"message": f"Scraper {task_id} started in background!"})

# if __name__ == '__main__':
#     app.run(host='127.0.0.1', port=5000, debug=True)
