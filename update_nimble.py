import sys

with open('src/nimble/NimbleBluetooth.cpp', 'r') as f:
    content = f.read()

# Add global variable
content = content.replace(
    'NimBLECharacteristic *fromNumCharacteristic;',
    'NimBLECharacteristic *fromNumCharacteristic;\nNimBLECharacteristic *fromRadioSyncCharacteristic;'
)

# Add characteristic creation (NO_PIN)
content = content.replace(
    'fromNumCharacteristic = bleService->createCharacteristic(FROMNUM_UUID, NIMBLE_PROPERTY::NOTIFY | NIMBLE_PROPERTY::READ);',
    'fromNumCharacteristic = bleService->createCharacteristic(FROMNUM_UUID, NIMBLE_PROPERTY::NOTIFY | NIMBLE_PROPERTY::READ);\n        fromRadioSyncCharacteristic = bleService->createCharacteristic(FROMRADIOSYNC_UUID, NIMBLE_PROPERTY::INDICATE | NIMBLE_PROPERTY::READ);'
)

# Add characteristic creation (With PIN)
# We need to find the specific block
search_str = '''        fromNumCharacteristic =
            bleService->createCharacteristic(FROMNUM_UUID, NIMBLE_PROPERTY::NOTIFY | NIMBLE_PROPERTY::READ |
                                                               NIMBLE_PROPERTY::READ_AUTHEN | NIMBLE_PROPERTY::READ_ENC);'''
replace_str = '''        fromNumCharacteristic =
            bleService->createCharacteristic(FROMNUM_UUID, NIMBLE_PROPERTY::NOTIFY | NIMBLE_PROPERTY::READ |
                                                               NIMBLE_PROPERTY::READ_AUTHEN | NIMBLE_PROPERTY::READ_ENC);
        fromRadioSyncCharacteristic = bleService->createCharacteristic(
            FROMRADIOSYNC_UUID, NIMBLE_PROPERTY::INDICATE | NIMBLE_PROPERTY::READ | NIMBLE_PROPERTY::READ_AUTHEN |
                                    NIMBLE_PROPERTY::READ_ENC | NIMBLE_PROPERTY::INDICATE_AUTHEN | NIMBLE_PROPERTY::INDICATE_ENC);'''
content = content.replace(search_str, replace_str)

# Update runOnceHasWorkToPhone
content = content.replace(
    'return onReadCallbackIsWaitingForData || runOnceToPhoneCanPreloadNextPacket();',
    'return onReadCallbackIsWaitingForData || runOnceToPhoneCanPreloadNextPacket() || (fromRadioSyncCharacteristic && fromRadioSyncCharacteristic->getSubscribeCount() > 0 && available());'
)

# Update runOnceHandleToPhoneQueue condition
content = content.replace(
    'if (onReadCallbackIsWaitingForData || runOnceToPhoneCanPreloadNextPacket()) {',
    'if (onReadCallbackIsWaitingForData || runOnceToPhoneCanPreloadNextPacket() || (fromRadioSyncCharacteristic && fromRadioSyncCharacteristic->getSubscribeCount() > 0)) {'
)

# Add indicate call
content = content.replace(
    'toPhoneQueueSize++;',
    '''toPhoneQueueSize++;
                        if (fromRadioSyncCharacteristic && fromRadioSyncCharacteristic->getSubscribeCount() > 0) {
                            fromRadioSyncCharacteristic->setValue(fromRadioBytes, numBytes);
                            fromRadioSyncCharacteristic->indicate();
                        }'''
)

with open('src/nimble/NimbleBluetooth.cpp', 'w') as f:
    f.write(content)
