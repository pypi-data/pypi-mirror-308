INSERT INTO localizations (position, phase_name, language_code, text_value) VALUES 
('LOC_TITLE', 'all', 'en_US', 'Title'),
('LOC_TITLE', 'all', 'fr_FR', 'Titre'),
('LOC_SELECT_PLAYER', 'phase1', 'en_US', 'Choose your fighter!') 
-- Example of use of the localizations table
-- in the game, get the text via self.texts.get(position).
-- If it exist in the current language, it gets it
-- If it doesn't, it gets the text in the default language
-- If it doesn't exist in the default language, it gets the position instead
-- The current and default languages can be find in the config and settings files
-- You can delete these commented lines and add more entries