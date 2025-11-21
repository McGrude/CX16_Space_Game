.RECIPEPREFIX := >
BUILD_DIR := ../BUILD
COMMON := common.bas

DOCKED := $(BUILD_DIR)/DOCKED.BAS
SPACE := $(BUILD_DIR)/SPACE.BAS
COMBAT := $(BUILD_DIR)/COMBAT.BAS

all: $(BUILD_DIR) $(DOCKED) $(SPACE) $(COMBAT)
>@echo "Build complete."

$(BUILD_DIR):
>mkdir -p $(BUILD_DIR)

$(DOCKED): $(COMMON) docked_main.bas
>cat $(COMMON) docked_main.bas > $@

$(SPACE): $(COMMON) space_main.bas
>cat $(COMMON) space_main.bas > $@

$(COMBAT): $(COMMON) combat_main.bas
>cat $(COMMON) combat_main.bas > $@

clean:
>rm -f $(DOCKED) $(SPACE) $(COMBAT)

.PHONY: all clean
