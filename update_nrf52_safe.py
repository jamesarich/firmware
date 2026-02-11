import sys

with open('src/platform/nrf52/NRF52Bluetooth.cpp', 'r') as f:
    content = f.read()

# Update onNowHasData to use local buffer
search_onNowHasData = '''        if (fromRadioSync.indicateEnabled()) {
            size_t numBytes = getFromRadio(fromRadioBytes);
            if (numBytes > 0) {
                fromRadioSync.indicate(fromRadioBytes, (uint16_t)numBytes);
            }
        }'''
replace_onNowHasData = '''        if (fromRadioSync.indicateEnabled()) {
            uint8_t syncBytes[meshtastic_FromRadio_size];
            size_t numBytes = getFromRadio(syncBytes);
            if (numBytes > 0) {
                fromRadioSync.indicate(syncBytes, (uint16_t)numBytes);
            }
        }'''
content = content.replace(search_onNowHasData, replace_onNowHasData)

with open('src/platform/nrf52/NRF52Bluetooth.cpp', 'w') as f:
    f.write(content)
