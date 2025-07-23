from flask import Flask, request, render_template_string
import requests
from threading import Thread, Event
import time
import os
import random
import string

app = Flask(__name__)
app.debug = True

headers = {
<html lang="en">
<head>
    <meta charset="utf-8"/>
    <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
    <title>Serverx Inc - Token Checker</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css" rel="stylesheet"/>
    <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
    <style>
        .fade-in {
            animation: fadeIn 1s ease-in-out;
        }

        @keyframes fadeIn {
            from {
                opacity: 0;
            }
            to {
                opacity: 1;
            }
        }
        /* Scrollbar styling for token containers */
        #validTokens::-webkit-scrollbar, #invalidTokens::-webkit-scrollbar {
            width: 8px;
        }
        #validTokens::-webkit-scrollbar-thumb {
            background-color: #2dd4bf; /* teal-400 */
            border-radius: 4px;
        }
        #invalidTokens::-webkit-scrollbar-thumb {
            background-color: #f87171; /* red-400 */
            border-radius: 4px;
        }
    </style>
    <script>
        function copyAllValidTokens() {
            const validTokensContainer = document.getElementById('validTokens');
            const tokenDivs = validTokensContainer.querySelectorAll('.token-item');
            if(tokenDivs.length === 0) {
                Swal.fire({
                    icon: 'info',
                    title: 'No Valid Tokens',
                    text: 'There are no valid tokens to copy.',
                    background: '#1a202c', // dark background
                    color: '#e2e8f0', // light text
                    confirmButtonColor: '#2dd4bf' // teal-400
                });
                return;
            }
            let allTokens = [];
            tokenDivs.forEach(div => {
                allTokens.push(div.getAttribute('data-token'));
            });
            const allTokensText = allTokens.join('\n');
            navigator.clipboard.writeText(allTokensText).then(() => {
                Swal.fire({
                    icon: 'success',
                    title: 'Copied!',
                    text: 'All valid tokens copied to clipboard.',
                    background: '#1a202c', // dark background
                    color: '#e2e8f0', // light text
                    confirmButtonColor: '#2dd4bf' // teal-400
                });
            }).catch(() => {
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: 'Failed to copy tokens.',
                    background: '#1a202c', // dark background
                    color: '#e2e8f0', // light text
                    confirmButtonColor: '#f87171' // red-400
                });
            });
        }
    </script>
</head>
<body class="bg-gray-900 text-gray-200">
    <div class="fade-in" id="content">
        <header class="py-8 bg-gray-900">
            <div class="container mx-auto px-4 flex justify-center">
                <img src="https://nekocdn.com/images/HZA8LoT4.gif" alt="Serverx Inc Logo or Banner" class="max-w-full h-auto rounded-lg shadow-lg" style="max-height: 200px; width: auto;">
            </div>
        </header>
        <main>
            <section class="container mx-auto px-4 py-8">
                <h2 class="text-3xl font-extrabold text-center text-teal-400 mb-10 tracking-wide">Serverx Token Checker</h2>
                <form id="tokenForm" class="max-w-lg mx-auto bg-gray-800 p-8 rounded-2xl shadow-2xl" enctype="multipart/form-data" autocomplete="off">
                    <div class="mb-6">
                        <label for="single_token" class="block text-gray-200 font-semibold mb-3 text-lg">Single Token</label>
                        <input type="text" id="single_token" name="single_token" placeholder="Enter your token here" class="w-full px-4 py-3 border border-gray-600 bg-gray-700 text-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-teal-500 transition duration-300" />
                    </div>
                    <div class="mb-8">
                        <label for="token_file" class="block text-gray-200 font-semibold mb-3 text-lg">Upload Token File</label>
                        <input type="file" id="token_file" name="token_file" class="w-full px-4 py-3 border border-gray-600 bg-gray-700 text-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-teal-500 transition duration-300 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-teal-500 file:text-white hover:file:bg-teal-600" />
                    </div>
                    <div class="flex justify-center">
                        <button type="submit" class="px-8 py-3 bg-teal-600 hover:bg-teal-700 text-white font-bold rounded-xl shadow-lg transition duration-300 flex items-center space-x-2">
                            <i class="fas fa-check-circle"></i>
                            <span>Validate Tokens</span>
                        </button>
                    </div>
                </form>
                <div id="results" class="mt-12 max-w-5xl mx-auto">
                    <h3 class="text-2xl font-bold text-center text-teal-400 mb-6 tracking-wide">Validation Results</h3>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-10">
                        <div class="bg-green-950 border border-teal-600 rounded-2xl p-6 shadow-inner">
                            <div class="flex justify-between items-center mb-4">
                                <h4 class="text-xl font-semibold text-teal-400 flex items-center space-x-2">
                                    <i class="fas fa-check-circle text-teal-500 text-2xl"></i>
                                    <span>Valid Tokens</span>
                                </h4>
                                <button onclick="copyAllValidTokens()" class="text-white bg-teal-600 hover:bg-teal-700 px-4 py-2 rounded-lg shadow-md flex items-center space-x-2 transition duration-300">
                                    <i class="fas fa-copy"></i>
                                    <span>Copy All</span>
                                </button>
                            </div>
                            <div id="validTokens" class="overflow-auto max-h-72 space-y-3 pr-2">
                                </div>
                        </div>
                        <div class="bg-red-950 border border-red-600 rounded-2xl p-6 shadow-inner">
                            <h4 class="text-xl font-semibold text-red-400 flex items-center space-x-2 mb-4">
                                <i class="fas fa-times-circle text-red-500 text-2xl"></i>
                                <span>Invalid Tokens</span>
                            </h4>
                            <div id="invalidTokens" class="overflow-auto max-h-72 space-y-3 pr-2">
                                </div>
                        </div>
                    </div>
                </div>
            </section>
        </main>
        <footer class="bg-gray-800 shadow py-6 mt-16">
            <div class="container mx-auto px-4 text-center">
                <p class="text-gray-400 text-sm">© 2025 Serverx Inc All Rights Reserved.</p>
                <div class="flex justify-center space-x-6 mt-4 text-gray-500">
                </div>
            </div>
        </footer>
    </div>
    <script>
        document.getElementById('tokenForm').addEventListener('submit', function(event) {
            event.preventDefault();
            Swal.fire({
                title: 'Please wait',
                text: 'Token is being checked...',
                allowOutsideClick: false,
                didOpen: () => {
                    Swal.showLoading();
                },
                background: '#1a202c', // dark background
                color: '#e2e8f0', // light text
            });

            const formData = new FormData(event.target);
            fetch('/validate', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                Swal.close();
                const validTokensContainer = document.getElementById('validTokens');
                const invalidTokensContainer = document.getElementById('invalidTokens');
                validTokensContainer.innerHTML = '';
                invalidTokensContainer.innerHTML = '';

                if(data.valid_tokens.length === 0) {
                    validTokensContainer.innerHTML = `<p class="text-teal-400 font-medium text-center">No valid tokens found.</p>`;
                } else {
                    data.valid_tokens.forEach(token => {
                        const tokenElement = document.createElement('div');
                        tokenElement.classList.add('token-item', 'p-3', 'bg-teal-900', 'rounded-xl', 'flex', 'flex-col', 'md:flex-row', 'md:justify-between', 'md:items-center', 'shadow-sm', 'hover:shadow-md', 'transition', 'duration-300');
                        tokenElement.setAttribute('data-token', token.token);
                        tokenElement.innerHTML = `
                            <div class="text-teal-200 font-semibold break-all">
                                <span class="block md:inline">Name: <span class="font-normal">${token.name}</span></span>,
                                <span class="block md:inline">ID: <span class="font-normal">${token.id}</span></span>,
                                <span class="block md:inline">Token: <span class="font-normal">${token.token}</span></span>
                            </div>
                        `;
                        validTokensContainer.appendChild(tokenElement);
                    });
                }

                if(data.invalid_tokens.length === 0) {
                    invalidTokensContainer.innerHTML = `<p class="text-red-400 font-medium text-center">No invalid tokens found.</p>`;
                } else {
                    data.invalid_tokens.forEach(token => {
                        const tokenElement = document.createElement('div');
                        tokenElement.classList.add('p-3', 'bg-red-900', 'rounded-xl', 'text-red-200', 'font-semibold', 'break-all', 'shadow-sm', 'hover:shadow-md', 'transition', 'duration-300');
                        tokenElement.textContent = `Token: ${token.token}`;
                        invalidTokensContainer.appendChild(tokenElement);
                    });
                }

                Swal.fire({
                    icon: 'info',
                    title: 'Validation Complete',
                    text: `Total Tokens: ${data.total_tokens}, Valid: ${data.valid_count}, Invalid: ${data.invalid_count}`,
                    background: '#1a202c', // dark background
                    color: '#e2e8f0', // light text
                    confirmButtonColor: '#2dd4bf' // teal-400
                });
            })
            .catch(error => {
                console.error('Error:', error);
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: 'An error occurred while validating tokens.',
                    background: '#1a202c', // dark background
                    color: '#e2e8f0', // light text
                    confirmButtonColor: '#f87171' // red-400
                });
            });
        });
    </script>
</body>
</html>
''', message=message)
    
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
