class corpus:
    def __init__():
        initialize pseudoconnections
        initialize targetinfo
        initialize attemptsList

    def getTargetInfo():
        pass
    
    def setTargetInfo():
        pass

    def getPseudoconnections():
        pass
    
    def pcAdd():
        #logic to add token into corpus intentionally with meaning
        #design rag (or maybe some graph based structure) to establish connection
        #between different basic elements of potential jailbreak attempt prompts and
        #weighting based on probabilistic success for a certain element
        pass

    def addAttempt(outcome, prompt, context):
        pass

    def orderAttempts():
        order self.attemptsList

def tierCriteria(criteria):
    if given criteria is not tiered
    ask llm to turn binary criteria into tiered criteria

def processJailbreakDataIntoBasePrompts(jailbreakData):
    returns traversable list
    pass

def evaluateReward(token, response):
    pass

def llmCall(prompt):
    pass

def targetCall(attemptPrompt):
    returns target api response
    pass

def verifynoinadvertenteffects():
    #maybe consider passed on target info
    #to detect (inadvertently) malicious uses of the agent (real world effect, etc.)
    pass

def evaluateRewardConfidence():
    #include fallback logic, retries, or logging ambiguous responses for manual review
    pass

def fastMode(): #beam search
    while(not lower than a certain possible reward):
        verifynoinadvertenteffects
        targetCall(attemptPrompt)
        evaluateReward
        evaluateRewardConfidence
        corpus.addAttempt(prompt, evaluateReward, evaluateRewardConfidence) #Traceability
        corpus.pcAdd(token, context, reward)
        iteratively tries next most reward likely based on criteria (append token to attemptPrompt?)

def thoroughMode(): #dfs with backtracking
    base case: no more branches
    for each top n appendments:
        verifynoinadvertenteffects
        targetCall(attemptPrompt)
        evaluateReward
        evaluateRewardConfidence
        corpus.addAttempt(prompt, evaluateReward, evaluateRewardConfidence) #Traceability
        corpus.pcAdd(token, context, reward)
        thoroughMode(next untried branch (append token to attemptPrompt?))

def main():

    corpus.targetInfo = take in target api structure and (tiered) criteria for faulty response
    take in jailbreaking data from file

    processJailbreakDataIntoBasePrompts/llmCall()?
    
    ask for which mode
    for item in jailbreakData:
        if wantfastmode:
            fastMode()
        elif wantThoroughMode:
            thoroughMode()
        