from concurrent.futures import ThreadPoolExecutor
from disgrasya.gen import gen_cards
from disgrasya.ppcp import ppcp_api
from disgrasya.nmi import nmi_api
import argparse

def main():
    parser = argparse.ArgumentParser(description="Check credit card using different gateways or generate card details")
    parser.add_argument('--api', required=False, help="nmi, ppcp")
    parser.add_argument('--url', required=False, help="The product url.")
    parser.add_argument('--creditcard', required=False, help="Path to the credit card text file.")
    parser.add_argument('--threads', type=int, required=False, help="The amount of threads the user wants.")
    parser.add_argument('--proxy', required=False, help="Optional: use proxy when processing credit cards.")
    parser.add_argument('--gen', nargs='+', help="Generate credit card details with format: cc mm yy count or cc count")

    args = parser.parse_args()

    try:
        if args.gen:
            bin_code = args.gen[0]
            count = int(args.gen[-1])

            if len(args.gen) == 2:
                month = "random"
                year = "random"
            else:
                month = args.gen[1]
                year = args.gen[2]

            gen_cards(bin_code, month, year, count)

        elif args.api:
            if not all([args.url, args.creditcard, args.threads]):
                parser.error("--api requires --url, --creditcard, and --threads arguments")

            creditCards = open(args.creditcard, "r").readlines()
            if args.api == 'nmi':
                with ThreadPoolExecutor(max_workers=args.threads) as executor:
                    for creditCard in creditCards:
                        executor.submit(nmi_api, args.url, creditCard.strip(), args.proxy)
            elif args.api == 'ppcp':
                with ThreadPoolExecutor(max_workers=args.threads) as executor:
                    for creditCard in creditCards:
                        executor.submit(ppcp_api, args.url, creditCard.strip(), args.proxy)

    except Exception as e:
        print(f"An error occurred during processing: {e}")

if __name__ == "__main__":
    main()
