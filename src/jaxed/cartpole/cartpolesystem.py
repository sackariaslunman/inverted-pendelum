from __future__ import annotations
import jax
import jax.numpy as jnp
from eom import generate_dynamics_with_1_poles, generate_dynamics_with_2_poles

def generate_random_cartpole_system(
        key, 
        n_poles: int,
        cart_mass_range: tuple[float, float],
        gravity_range: tuple[float, float],
        gravity_orientation_range: tuple[float, float],
        masses_range: tuple[float, float],
        lengths_range: tuple[float, float],
        frictions_range: tuple[float, float],
        inertias_range: tuple[float, float]
        ) -> CartPoleSystem:
    assert n_poles > 0
    cart_mass = jax.random.uniform(key, minval=cart_mass_range[0], maxval=cart_mass_range[1])
    gravity = jax.random.uniform(key, minval=gravity_range[0], maxval=gravity_range[1])
    gravity_orientation = jax.random.uniform(key, minval=gravity_orientation_range[0], maxval=gravity_orientation_range[1])
    masses = jax.random.uniform(key, shape=(n_poles,), minval=masses_range[0], maxval=masses_range[1])
    lengths = jax.random.uniform(key, shape=(n_poles,), minval=lengths_range[0], maxval=lengths_range[1])
    centres_of_mass = jax.random.uniform(key, shape=(n_poles,), minval=lengths_range[0] * 0.1, maxval=lengths_range[1] * 0.9)
    frictions = jax.random.uniform(key, shape=(n_poles,), minval=frictions_range[0], maxval=frictions_range[1])
    inertias = jax.random.uniform(key, shape=(n_poles,), minval=inertias_range[0], maxval=inertias_range[1])
    return CartPoleSystem(n_poles, cart_mass, gravity, gravity_orientation, masses, lengths, centres_of_mass, frictions, inertias)

class CartPoleSystem:
    def __init__(
            self, 
            n_poles: int,
            cart_mass: float, 
            gravity: float, 
            gravity_orientation: float,
            masses: jnp.ndarray, 
            lengths: jnp.ndarray, 
            centres_of_mass: jnp.ndarray, 
            frictions: jnp.ndarray,
            inertias: jnp.ndarray
            ) -> None:
        assert 1 <= n_poles <= 2
        self._n_poles = n_poles

        assert cart_mass > 0
        self._cart_mass = cart_mass

        assert gravity > 0
        self._gravity = gravity

        assert -0.5*jnp.pi <= gravity_orientation <= 0.5*jnp.pi
        self._gravity_orientation = gravity_orientation

        assert masses.shape == (n_poles,)
        self._masses = masses
        
        assert lengths.shape == (n_poles,)
        self._lengths = lengths

        assert centres_of_mass.shape == (n_poles,)
        self._centres_of_mass = centres_of_mass

        assert frictions.shape == (n_poles,)
        self._frictions = frictions

        assert inertias.shape == (n_poles,)
        self._inertias = inertias

        match n_poles:
            case 1:
                generate_dynamics = generate_dynamics_with_1_poles
            case 2:
                generate_dynamics = generate_dynamics_with_2_poles

        self.dynamics, self.observe, self.distance = generate_dynamics(
            cart_mass, gravity, gravity_orientation, masses, lengths, centres_of_mass, frictions, inertias
        )
    
    @property
    def n_poles(self) -> int:
        return self._n_poles
    
    @property
    def cart_mass(self) -> float:
        return self._cart_mass
    
    @property
    def gravity(self) -> float:
        return self._gravity
    
    @property
    def masses(self) -> jnp.ndarray:
        return self._masses
    
    @property
    def lengths(self) -> jnp.ndarray:
        return self._lengths
    
    @property
    def centres_of_mass(self) -> jnp.ndarray:
        return self._centres_of_mass
    
    @property
    def frictions(self) -> jnp.ndarray:
        return self._frictions
    
    @property
    def inertias(self) -> jnp.ndarray:
        return self._inertias

    def __call__(self, state: jnp.ndarray, action: jnp.ndarray) -> jnp.ndarray:
        return self.dynamics(state, action)

def test_cart1polesystem():
    n_poles = 1
    cart_mass = 1.0
    gravity = 9.81
    gravity_orientation = 0.0
    masses = jnp.array([1.0])
    lengths = jnp.array([1.0])
    half_lengths = lengths * 0.56
    frictions = jnp.array([1.0])
    inertias = jnp.array([1.0])
    system = CartPoleSystem(n_poles, cart_mass, gravity, gravity_orientation, masses, lengths, half_lengths, frictions, inertias)
    state = jnp.array([0.0, 0.0, 0.0, 0.0])
    action = jnp.array([1])
    print("dstate:", system(state, action))

def test_cart2polesystem():
    n_poles = 2
    cart_mass = 1.0
    gravity = 9.81
    gravity_orientation = 0.0
    masses = jnp.array([1.0, 1.0])
    lengths = jnp.array([1.0, 1.0])
    half_lengths = lengths * 0.56
    frictions = jnp.array([1.0, 1.0])
    inertias = jnp.array([1.0, 1.0])
    system = CartPoleSystem(n_poles, cart_mass, gravity, gravity_orientation, masses, lengths, half_lengths, frictions, inertias)
    state = jnp.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    action = jnp.array([1])
    print("dstate:", system(state, action))

if __name__ == "__main__":
    test_cart1polesystem()
    test_cart2polesystem()