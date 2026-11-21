
import streamlit as st


wallet_component = st.components.v2.component(
    name="crypto_pulse_wallet",

    html="""
        <div class="wallet-box">
            <h3>Connect Your Wallet</h3>

            <button id="metamask-button">
                🦊 Connect MetaMask
            </button>

            <button id="phantom-button">
                👻 Connect Phantom
            </button>

            <p id="wallet-status">
                No wallet connected
            </p>
        </div>
    """,

    css="""
        .wallet-box {
            padding: 20px;
            border-radius: 14px;
            background: #172033;
            border: 1px solid #6366f1;
        }

        .wallet-box h3 {
            color: white;
            margin-bottom: 16px;
        }

        .wallet-box button {
            display: block;
            width: 100%;
            margin-bottom: 12px;
            padding: 13px;
            border: none;
            border-radius: 9px;
            color: white;
            font-weight: bold;
            cursor: pointer;
            background: linear-gradient(100deg, #7c3aed, #2563eb);
        }

        .wallet-box button:disabled {
            opacity: 0.6;
            cursor: wait;
        }

        #wallet-status {
            color: #cbd5e1;
            margin-top: 14px;
            overflow-wrap: anywhere;
        }
    """,

    js="""
        export default function(component) {

            const { parentElement, setStateValue } = component;

            const metamaskButton =
                parentElement.querySelector("#metamask-button");

            const phantomButton =
                parentElement.querySelector("#phantom-button");

            const status =
                parentElement.querySelector("#wallet-status");


            // Find MetaMask specifically.
            function getMetaMaskProvider() {

                const ethereum = window.ethereum;

                if (!ethereum) {
                    return null;
                }

                // Multiple EVM wallet providers are installed.
                if (Array.isArray(ethereum.providers)) {

                    return ethereum.providers.find(
                        provider =>
                            provider.isMetaMask &&
                            !provider.isPhantom
                    ) || null;
                }

                // Only one EVM provider is available.
                if (
                    ethereum.isMetaMask &&
                    !ethereum.isPhantom
                ) {
                    return ethereum;
                }

                return null;
            }


            // Connect MetaMask only.
            async function connectMetaMask() {

                const provider = getMetaMaskProvider();

                if (!provider) {

                    status.textContent =
                        "MetaMask not detected. Please install or enable MetaMask.";

                    setStateValue("wallet", {
                        status: "not_installed",
                        wallet_type: "MetaMask"
                    });

                    return;
                }

                try {

                    metamaskButton.disabled = true;
                    phantomButton.disabled = true;

                    status.textContent = "Connecting MetaMask...";

                    const accounts = await provider.request({
                        method: "eth_requestAccounts"
                    });

                    if (!accounts || accounts.length === 0) {
                        throw new Error("No MetaMask account available.");
                    }

                    const chainId = await provider.request({
                        method: "eth_chainId"
                    });

                    const walletData = {
                        status: "connected",
                        wallet_type: "MetaMask",
                        network: "EVM",
                        address: accounts[0],
                        chain_id: chainId
                    };

                    status.textContent =
                        "MetaMask connected: " +
                        accounts[0].slice(0, 6) +
                        "..." +
                        accounts[0].slice(-4);

                    setStateValue("wallet", walletData);

                } catch (error) {

                    status.textContent =
                        error.message || "MetaMask connection failed.";

                    setStateValue("wallet", {
                        status: "error",
                        wallet_type: "MetaMask",
                        message: error.message || "Connection failed."
                    });

                } finally {

                    metamaskButton.disabled = false;
                    phantomButton.disabled = false;
                }
            }


            // Connect Phantom only.
            async function connectPhantom() {

                const provider = window.phantom?.solana;

                if (!provider || !provider.isPhantom) {

                    status.textContent =
                        "Phantom not detected. Please install or enable Phantom.";

                    setStateValue("wallet", {
                        status: "not_installed",
                        wallet_type: "Phantom"
                    });

                    return;
                }

                try {

                    phantomButton.disabled = true;
                    metamaskButton.disabled = true;

                    status.textContent = "Connecting Phantom...";

                    const response = await provider.connect();

                    if (!response.publicKey) {
                        throw new Error("No Phantom account available.");
                    }

                    const address = response.publicKey.toString();

                    const walletData = {
                        status: "connected",
                        wallet_type: "Phantom",
                        network: "Solana",
                        address: address
                    };

                    status.textContent =
                        "Phantom connected: " +
                        address.slice(0, 6) +
                        "..." +
                        address.slice(-4);

                    setStateValue("wallet", walletData);

                } catch (error) {

                    status.textContent =
                        error.message || "Phantom connection failed.";

                    setStateValue("wallet", {
                        status: "error",
                        wallet_type: "Phantom",
                        message: error.message || "Connection failed."
                    });

                } finally {

                    phantomButton.disabled = false;
                    metamaskButton.disabled = false;
                }
            }


            // Button events.
            metamaskButton.addEventListener(
                "click",
                connectMetaMask
            );

            phantomButton.addEventListener(
                "click",
                connectPhantom
            );


            // Remove events when component is unmounted.
            return () => {

                metamaskButton.removeEventListener(
                    "click",
                    connectMetaMask
                );

                phantomButton.removeEventListener(
                    "click",
                    connectPhantom
                );
            };
        }
    """
)


def connect_wallet():
    return wallet_component(key="crypto_pulse_wallet")
