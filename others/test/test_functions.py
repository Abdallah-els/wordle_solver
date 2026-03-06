from solver import remaining_entropy

def test_remainig_entropy():
    """Testing the remainig entopy with 
    n_elments = 2000, H = 10.966 bits/symbole
    n_elments = 1000, H = 9.965 bits/symbole
    n_elments = 500, H = 8.957 bits/symbole
     """
    
    n_elments = [2000, 1000, 500]
    H = [10.96578428, 9.965784285, 8.955784285]

    for i in range(len(n_elments)):
        entropy = remaining_entropy(n_elments[i])

        assert abs(H[i] - entropy) <= 1e-2

if __name__ == "__main__":
    test_remainig_entropy()