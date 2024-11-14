from pydantic import BaseModel

class AutoAiScan(BaseModel):
    url: str

class ModelFeatures(BaseModel):
    IsDomainIP: float
    NoOfAmpersandInURL: float
    TLDLegitimateProb: float
    TLDLength: float
    LargestLineLength: float
    Robots: float
    NoOfURLRedirect: float
    NoOfPopup: float
    HasExternalFormSubmit: float
    HasHiddenFields: float
    HasPasswordField: float
    Bank: float
    Pay: float
    Crypto: float
    NoOfiFrame: float
    NoOfEmptyRef: float