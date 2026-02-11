import sys

with open('src/nimble/NimbleBluetooth.cpp', 'r') as f:
    lines = f.readlines()

new_lines = []
skip = 0
for i in range(len(lines)):
    if skip > 0:
        skip -= 1
        continue

    # Check for duplicated indicate block
    if "if (fromRadioSyncCharacteristic && fromRadioSyncCharacteristic->getSubscribeCount() > 0) {" in lines[i]:
        if i + 4 < len(lines) and "if (fromRadioSyncCharacteristic && fromRadioSyncCharacteristic->getSubscribeCount() > 0) {" in lines[i+4]:
             # It is duplicated
             new_lines.append(lines[i])
             new_lines.append(lines[i+1])
             new_lines.append(lines[i+2])
             new_lines.append(lines[i+3])
             skip = 7 # skip this one and the next 4 lines
             continue

    new_lines.append(lines[i])

with open('src/nimble/NimbleBluetooth.cpp', 'w') as f:
    f.writelines(new_lines)
