import hashlib


def generate_hash(value):
    return int(hashlib.sha256(value.encode('utf-8')).hexdigest(), 16)

class ConsistentHashing:
    def __init__(self):
        self.server_map = {}
        self.sorted_server_hashes = []
        self.key_to_server_map = {}

    def add_server(self, server_name):
        server_hash = generate_hash(server_name)
        if server_hash not in self.server_map:
            self.server_map[server_hash] = server_name
            self.sorted_server_hashes.append(server_hash)
            self.sorted_server_hashes.sort()
            self.reassign_keys()

    def remove_server(self, server_name):
        server_hash = generate_hash(server_name)
        if server_hash in self.server_map:
            del self.server_map[server_hash]
            self.sorted_server_hashes.remove(server_hash)
            self.reassign_keys()

    def assign_key_to_server(self, key):
        key_hash = generate_hash(key)
        server_hash = self.find_closest_server_hash(key_hash)
        assigned_server = self.server_map[server_hash]
        self.key_to_server_map[key] = assigned_server

    def find_closest_server_hash(self, key_hash):
        for server_hash in self.sorted_server_hashes:
            if key_hash <= server_hash:
                return server_hash
        return self.sorted_server_hashes[0]

    def reassign_keys(self):
        all_keys = list(self.key_to_server_map.keys())
        self.key_to_server_map.clear()
        for key in all_keys:
            self.assign_key_to_server(key)

    def display_server_ring(self):
        print("Server Ring:")
        for server_hash in self.sorted_server_hashes:
            print(f"Hash: {server_hash} -> Server: {self.server_map[server_hash]}")

    def display_key_assignments(self):
        print("Key-Server Mapping Table:")
        for key, server in self.key_to_server_map.items():
            print(f"Key: {key} -> Assigned to server: {server}")


def interactive_mode():
    consistent_hashing = ConsistentHashing()
    
    while True:
        print("\n        Menu:")
        print("--------------------------------------------------------------------")
        print("1. Add a server")
        print("2. Remove a server")
        print("3. Assign a key to a server")
        print("4. Display server ring")
        print("5. Display key-server mapping table")
        print("6. Exit")
        print("--------------------------------------------------------------------")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            server_name = input("Enter server name to add: ")
            consistent_hashing.add_server(server_name)
            print(f"Server '{server_name}' added.")

        elif choice == '2':
            server_name = input("Enter server name to remove: ")
            consistent_hashing.remove_server(server_name)
            print(f"Server '{server_name}' removed.")

        elif choice == '3':
            key = input("Enter key to assign to a server: ")
            consistent_hashing.assign_key_to_server(key)
            print(f"Key '{key}' assigned to server.")

        elif choice == '4':
            consistent_hashing.display_server_ring()

        elif choice == '5':
            consistent_hashing.display_key_assignments()

        elif choice == '6':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")

# Run the interactive mode
interactive_mode()

