def main():
    with open('data/raw/shakespeare_complete.txt', 'r', encoding='utf-8') as file:
        content = file.read()

        print(f"Total file size: {len(content)} characters")
        print(f"First 500 characters:")
        print(content[:500])
        print("\n" + "="*50 + "\n")
        print(f"Last 500 characters:")
        print(content[-500:])
        


if __name__ == "__main__":
    main()
