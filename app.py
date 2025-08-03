from fastapi import FastAPI, Request
from pydantic import BaseModel
import grammalecte
import grammalecte.text as txt

app = FastAPI(title="Grammalecte API", description="A FastAPI wrapper for Grammalecte grammar checker")

# Initialize Grammalecte checker
checker = grammalecte.GrammarChecker("fr", "FastAPI")
spell_checker = checker.getSpellChecker()
text_formatter = checker.getTextFormatter()
gc_engine = checker.getGCEngine()

class TextRequest(BaseModel):
    text: str
    format_text: bool = False
    options: dict = None

class Correction(BaseModel):
    start: int
    end: int
    text: str  # The actual text at the error position
    message: str
    suggestions: list[str]
    rule_id: str | None = None

class CheckResponse(BaseModel):
    program: str = "grammalecte-fr"
    version: str
    lang: str
    data: list[Correction]

@app.get("/")
async def root():
    return {"message": "Grammalecte API is running"}

@app.post("/check", response_model=CheckResponse)
async def check_text(req: TextRequest):
    """
    Check text for grammar and spelling errors using Grammalecte
    """
    try:
        # Parse text and get errors
        data = []
        paragraphs = list(txt.getParagraph(req.text))
        current_position = 0
        
        for i, paragraph in enumerate(paragraphs, 1):
            if req.format_text:
                paragraph = text_formatter.formatText(paragraph)
            
            # Get errors for this paragraph
            result = checker.getParagraphErrorsAsJSON(
                i, 
                paragraph, 
                dOptions=req.options, 
                bEmptyIfNoErrors=True, 
                bReturnText=req.format_text
            )
            
            # Parse the JSON result and convert to our format
            import json
            try:
                if result and result.strip():
                    errors = json.loads(result)
                    
                    # Handle grammar errors
                    if 'lGrammarErrors' in errors:
                        for error in errors['lGrammarErrors']:
                            # Calculate positions relative to whole text
                            relative_start = current_position + error.get('nStart', 0)
                            relative_end = current_position + error.get('nEnd', 0)
                            
                            # Extract the actual text at the error position
                            error_text = req.text[relative_start:relative_end]
                            
                            correction = Correction(
                                start=relative_start,
                                end=relative_end,
                                text=error_text,
                                message=error.get('sMessage', ''),
                                suggestions=error.get('aSuggestions', []),
                                rule_id=error.get('sRuleId', None)
                            )
                            data.append(correction)
                    
                    # Handle spelling errors
                    if 'lSpellingErrors' in errors:
                        for error in errors['lSpellingErrors']:
                            # Calculate positions relative to whole text
                            relative_start = current_position + error.get('nStart', 0)
                            relative_end = current_position + error.get('nEnd', 0)
                            
                            # Extract the actual text at the error position
                            error_text = req.text[relative_start:relative_end]
                            
                            correction = Correction(
                                start=relative_start,
                                end=relative_end,
                                text=error_text,
                                message=f"Spelling error: {error.get('sValue', '')}",
                                suggestions=error.get('aSuggestions', []),
                                rule_id=error.get('sRuleId', None)
                            )
                            data.append(correction)
                            
            except json.JSONDecodeError as e:
                # If JSON parsing fails, skip this result
                pass
            
            # Update position for next paragraph
            current_position += len(paragraph) + 1  # +1 for the newline character
        
        return CheckResponse(
            version=gc_engine.version,
            lang=gc_engine.lang,
            data=data
        )
    
    except Exception as e:
        return CheckResponse(
            version=gc_engine.version,
            lang=gc_engine.lang,
            data=[],
            error=str(e)
        )

@app.get("/suggest/{token}")
async def get_suggestions(token: str):
    """
    Get spelling suggestions for a token
    """
    try:
        suggestions = []
        for suggestion_list in spell_checker.suggest(token):
            suggestions.extend(suggestion_list)
        return {"suggestions": suggestions}
    except Exception as e:
        return {"error": str(e)}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "service": "grammalecte-api",
        "version": gc_engine.version,
        "lang": gc_engine.lang
    }

@app.get("/options")
async def get_options():
    """
    Get available grammar checking options
    """
    return {
        "options": gc_engine.getOptions(),
        "default_options": gc_engine.getDefaultOptions()
    } 