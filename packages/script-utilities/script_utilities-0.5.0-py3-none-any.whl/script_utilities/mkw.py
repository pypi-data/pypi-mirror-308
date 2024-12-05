import enum as en

class Region(en.Enum):
    JAP = "J"
    KOR = "K"
    PAL = "P"
    USA = "U"

class Language(en.Enum):
    Dutch = "N", "Dutch", "nl"
    PFrench = "F", "French (PAL)", "fr"
    NFrench = "Q", "French (NTSC)", "ca"
    German = "G", "German", "de"
    Italian = "I", "Italian", "it"
    Japanese = "J", "Japanese", "ja"
    Korean = "K", "Korean", "ko"
    PPortuguese = "P", "Portuguese (PAL)", "pt"
    NPortuguese = "B", "Portuguese (NTSC)", "br"
    Russian = "R", "Russian", "ru"
    PSpanish = "S", "Spanish (PAL)", "es"
    NSpanish = "M", "Spanish (NTSC)", "mx"
    Greek = "L", "Greek", "el"
    Polish = "O", "Polish", "pl"
    Finnish = "H", "Finnish", "fi"
    Swedish = "W", "Swedish", "sv"
    Czech = "Z", "Czech", "cs"
    Danish = "D", "Danish", "da"
    
    def letter(self) -> str:
        """Returns the language identifier."""
        
        return self.value[0]
    
    def language(self) -> str:
        """Returns the full language name."""
        
        return self.value[1]
    
    def abbreviation(self) -> str:
        """Returns the language abbreviation."""
        
        return self.value[2]
