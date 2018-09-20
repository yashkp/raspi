import rfid


device = rfid.initialize_from_voting()
cardId = rfid.get_input(device)
print cardId

