from dispenser import move_bin

#Louis Testing code for 360 rotation of the top assembly
def main():
    try:
        # Example: Move to bin 3
        target = 4
        print(f"Starting movement to bin {target}...")
        move_bin(target)
        print("Movement complete.")
        
    except KeyboardInterrupt:
        print("\nManual override: Stopping motor.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()