from typing import Dict, Any, Optional, Union
import json
from web3 import Web3
from web3.contract import Contract
import os

class ContractManager:
    """Manages contract interactions using Web3"""
    
    def __init__(self, web3_provider: str):
        """
        Initialize the contract manager
        
        Args:
            web3_provider: Web3 provider URL (e.g. "https://mainnet.infura.io/v3/YOUR-PROJECT-ID")
        """
        self.w3 = Web3(Web3.HTTPProvider(web3_provider))
        self.contracts: Dict[str, Contract] = {}
        self.abis: Dict[str, Any] = {}
        self._load_abis()

    def _load_abis(self) -> None:
        """Load all ABI definitions from the config/abi directory"""
        abi_dir = os.path.join(os.path.dirname(__file__), "config", "abi")
        for filename in os.listdir(abi_dir):
            if filename.endswith(".json"):
                contract_name = filename.replace(".json", "")
                with open(os.path.join(abi_dir, filename)) as f:
                    self.abis[contract_name] = json.load(f)

    def get_contract(self, contract_type: str, address: str) -> Contract:
        """
        Get or create a contract instance
        
        Args:
            contract_type: Type of contract (e.g. "uni_v2", "uni_v3")
            address: Contract address
            
        Returns:
            Web3 Contract instance
        
        Raises:
            ValueError: If contract type is not supported
        """
        contract_key = f"{contract_type}"
        
        if contract_key in self.contracts:
            return self.contracts[contract_key]
        
        if contract_type not in self.abis:
            raise ValueError(f"Unsupported contract type: {contract_type}")
            
        contract = self.w3.eth.contract(
            address=Web3.to_checksum_address(address),
            abi=self.abis[contract_type]
        )
        
        self.contracts[contract_key] = contract
        return contract

    def read_contract(
        self,
        contract_type: str,
        address: str,
        method: str,
        args: Optional[list] = None,
        block_identifier: Optional[Union[int, str]] = 'latest'
    ) -> Any:
        """
        Read data from a contract
        
        Args:
            contract_type: Type of contract
            address: Contract address
            method: Contract method to call
            args: Method arguments
            block_identifier: Block number or 'latest'
            
        Returns:
            Method return value
        """
        contract = self.get_contract(contract_type, address)
        args = args or []
        
        contract_method = getattr(contract.functions, method)
        return contract_method(*args).call(block_identifier=block_identifier)

    def write_contract(
        self,
        contract_type: str,
        address: str,
        method: str,
        args: Optional[list] = None,
        private_key: str = None,
        value: int = 0,
        gas_limit: Optional[int] = None,
        gas_price: Optional[int] = None
    ) -> str:
        """
        Write to a contract (send transaction)
        
        Args:
            contract_type: Type of contract
            address: Contract address
            method: Contract method to call
            args: Method arguments
            private_key: Private key for signing transaction
            value: Amount of ETH to send (in wei)
            gas_limit: Gas limit for transaction
            gas_price: Gas price in wei
            
        Returns:
            Transaction hash
            
        Raises:
            ValueError: If private key is not provided
        """
        if not private_key:
            raise ValueError("Private key is required for contract writes")
            
        contract = self.get_contract(contract_type, address)
        args = args or []
        
        account = self.w3.eth.account.from_key(private_key)
        contract_method = getattr(contract.functions, method)
        
        transaction = contract_method(*args).build_transaction({
            'from': account.address,
            'value': value,
            'nonce': self.w3.eth.get_transaction_count(account.address),
            'gas': gas_limit or self.w3.eth.estimate_gas({
                'to': address,
                'from': account.address,
                'value': value
            }),
            'gasPrice': gas_price or self.w3.eth.gas_price
        })
        
        signed_txn = self.w3.eth.account.sign_transaction(transaction, private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        
        return self.w3.to_hex(tx_hash) 