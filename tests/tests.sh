export DEBUG=True && faketime '2024-08-31 21:00:00' python3 -m unittest test_application_layer.py
faketime '2024-08-31 21:00:00' python3 -m unittest test_utility.py
export DEBUG=True && chmod +x verify_debug.sh && cd fresh_install && faketime '2024-08-31 21:00:00' python3 -m unittest test.py