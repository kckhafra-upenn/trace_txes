from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import json
from datetime import datetime

rpc_user='quaker_quorum'
rpc_password='franklin_fought_for_continental_cash'
rpc_ip='3.134.159.30'
rpc_port='8332'

rpc_connection = AuthServiceProxy("http://%s:%s@%s:%s"%(rpc_user, rpc_password, rpc_ip, rpc_port))

###################################

class TXO:
    def __init__(self, tx_hash, n, amount, owner, time ):
        self.tx_hash = tx_hash 
        self.n = n
        self.amount = amount
        self.owner = owner
        self.time = time
        self.inputs = []
        

    def __str__(self, level=0):
        ret = "\t"*level+repr(self.tx_hash)+"\n"
        for tx in self.inputs:
            ret += tx.__str__(level+1)
        return ret

    def to_json(self):
        fields = ['tx_hash','n','amount','owner']
        json_dict = { field: self.__dict__[field] for field in fields }
        json_dict.update( {'time': datetime.timestamp(self.time) } )
        if len(self.inputs) > 0:
            for txo in self.inputs:
                json_dict.update( {'inputs': json.loads(txo.to_json()) } )
        return json.dumps(json_dict, sort_keys=True, indent=4)

    @classmethod
    def from_tx_hash(cls,tx_hash,n=0):
        #YOUR CODE HERE
        tx = rpc_connection.getrawtransaction(tx_hash,True)
        amount = 0
        address = ""
        time = datetime.fromtimestamp(tx["time"])
        for t in tx["vout"]:
            if(n==t["n"]):
                amount = int(str(t["value"]).replace(".",""))
                address = t["scriptPubKey"]["addresses"][0]
        c = cls(tx_hash,n,amount,address,time)
        return c
    def get_inputs(self,d=1):
        tx = rpc_connection.getrawtransaction(self.tx_hash,True)
        count=0
        print("I-TX: ",tx)
        pass
        #YOUR CODE HERE
        amount = 0
        address = ""
        time = datetime.fromtimestamp(tx["time"])
        for t in tx["vout"]:
            count+=1
            amount = int(str(t["value"]).replace(".",""))
            address = t["scriptPubKey"]["addresses"][0]
            self.amount=amount
            self.address=address
            
            print("AMOUNT: ",self.amount)
            print("AMOUNT: ",self.address)
            print("Input: ",self.inputs[i])
            self.inputs.append(self)
            if count==d:
                break
        print("TIME: ",self.time)
        print("HASH: ",self.tx_hash)
        return self.inputs
            