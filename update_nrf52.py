import sys

with open('src/platform/nrf52/NRF52Bluetooth.cpp', 'r') as f:
    content = f.read()

# Add static variable
content = content.replace(
    'static BLECharacteristic fromRadio = BLECharacteristic(BLEUuid(FROMRADIO_UUID_16));',
    'static BLECharacteristic fromRadio = BLECharacteristic(BLEUuid(FROMRADIO_UUID_16));\nstatic BLECharacteristic fromRadioSync = BLECharacteristic(BLEUuid(FROMRADIOSYNC_UUID_16));'
)

# Update onNowHasData
search_onNowHasData = '''    virtual void onNowHasData(uint32_t fromRadioNum) override
    {
        PhoneAPI::onNowHasData(fromRadioNum);

        LOG_INFO("BLE notify fromNum");
        fromNum.notify32(fromRadioNum);
    }'''
replace_onNowHasData = '''    virtual void onNowHasData(uint32_t fromRadioNum) override
    {
        PhoneAPI::onNowHasData(fromRadioNum);

        LOG_INFO("BLE notify fromNum");
        fromNum.notify32(fromRadioNum);

        if (fromRadioSync.indicateEnabled()) {
            size_t numBytes = getFromRadio(fromRadioBytes);
            if (numBytes > 0) {
                fromRadioSync.indicate(fromRadioBytes, (uint16_t)numBytes);
            }
        }
    }'''
content = content.replace(search_onNowHasData, replace_onNowHasData)

# Update onFromRadioAuthorize to use chr instead of fromRadio
content = content.replace(
    'fromRadio.write(fromRadioBytes, numBytes);',
    'chr->write(fromRadioBytes, numBytes);'
)

# Update setupMeshService
search_setup = '''    fromRadio.setBuffer(fromRadioBytes, sizeof(fromRadioBytes)); // we preallocate our fromradio buffer so we won't waste space
    // for two copies
    fromRadio.begin();'''
replace_setup = '''    fromRadio.setBuffer(fromRadioBytes, sizeof(fromRadioBytes)); // we preallocate our fromradio buffer so we won't waste space
    // for two copies
    fromRadio.begin();

    fromRadioSync.setProperties(CHR_PROPS_INDICATE | CHR_PROPS_READ);
    fromRadioSync.setPermission(secMode, SECMODE_NO_ACCESS);
    fromRadioSync.setMaxLen(sizeof(fromRadioBytes));
    fromRadioSync.setReadAuthorizeCallback(onFromRadioAuthorize, false);
    fromRadioSync.setBuffer(fromRadioBytes, sizeof(fromRadioBytes));
    fromRadioSync.begin();'''
content = content.replace(search_setup, replace_setup)

with open('src/platform/nrf52/NRF52Bluetooth.cpp', 'w') as f:
    f.write(content)
