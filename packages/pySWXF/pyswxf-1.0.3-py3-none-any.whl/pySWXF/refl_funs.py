# -*- coding: utf-8 -*-
"""
Created on Mon Aug 20 09:47:57 2018

@author: th0lxl1
"""

from numpy import sqrt, tile, transpose, sin, exp, zeros
from numpy import linspace
from numpy import sum as nsum
from numpy import abs as nabs
import xraydb as xdb
import numpy as np
import scipy.constants as scc

def mlayer_rough(incident_angles, energy, refractive_indices, interface_positions, roughnesses):
    """
    Optimized version of the mlayer_rough function for calculating 
    the transmission and reflection matrices with roughness included.

    Parameters
    ----------
    incident_angles : numpy array
        Incident angles (in radians).
    energy : float
        Incident energy (eV).
    refractive_indices : numpy array of complex
        Refractive indices of the layers.
    interface_positions : numpy array of floats
        Positions of the interfaces (in meters).
    roughnesses : numpy array of floats
        Roughness of each interface (in meters).

    Returns
    ----------
    T : numpy array
        Transmission matrix.
    R : numpy array
        Reflectivity matrix.
    kz : numpy array
        Wavevector matrix (in inverse meters).
    """

    # Calculate the wavevector k0 from the energy
    wavevector = 2 * np.pi * energy * scc.e / scc.h / scc.c
    num_angles = len(incident_angles)
    num_layers = len(refractive_indices)

    # Compute kz values for each layer
    sin_alpha_squared = np.sin(incident_angles)[:, np.newaxis]**2
    refractive_diffs = refractive_indices**2 - refractive_indices[0]**2
    kz = wavevector * np.sqrt(sin_alpha_squared + refractive_diffs)

    # Tile interface positions and roughnesses to match incident_angles' shape
    zm = np.tile(interface_positions, (num_angles, 1))
    sig_squared = np.tile(roughnesses**2, (num_angles, 1))

    # Reflection coefficients between layers (including roughness)
    kz_diff = kz[:, :-1] - kz[:, 1:]
    kz_sum = kz[:, :-1] + kz[:, 1:]
    rr = kz_diff / kz_sum
    exp_factor = np.exp(-2 * np.abs(kz[:, :-1] * kz[:, 1:]) * sig_squared)
    rr *= exp_factor

    tp = 1 - rr

    # Initialize matrices with explicit memory order (C-contiguous)
    R = np.zeros((num_angles, num_layers), dtype=complex, order='C')
    T = np.zeros((num_angles, num_layers), dtype=complex, order='C')
    X = np.zeros((num_angles, num_layers), dtype=complex, order='C')

    # Calculate X matrix in a recursive manner
    for jl in range(num_layers - 2, -1, -1):
        exp_term = np.exp(2j * kz[:, jl+1] * zm[:, jl])
        rr_current = rr[:, jl]
        X_next = X[:, jl+1]
        
        X[:, jl] = rr_current + X_next * exp_term
        X[:, jl] *= np.exp(-2j * kz[:, jl] * zm[:, jl])
        X[:, jl] /= 1 + rr_current * X_next * exp_term

    # Set initial transmission and reflection coefficients
    T[:, 0] = 1.0
    R[:, 0] = X[:, 0]

    # Calculate T and R matrices
    for jl in range(num_layers - 1):
        exp_kz_diff = np.exp(-1j * (kz[:, jl+1] - kz[:, jl]) * zm[:, jl])
        exp_kz_sum = np.exp(-1j * (kz[:, jl+1] + kz[:, jl]) * zm[:, jl])
        R[:, jl+1] = (R[:, jl] * exp_kz_diff - T[:, jl] * rr[:, jl] * exp_kz_sum) / tp[:, jl]
        T[:, jl+1] = (T[:, jl] * np.exp(1j * (kz[:, jl+1] - kz[:, jl]) * zm[:, jl]) - R[:, jl] * rr[:, jl] * np.exp(1j * (kz[:, jl+1] + kz[:, jl]) * zm[:, jl])) / tp[:, jl]

    return T, R, kz


def mlayer_conv(incident_angles, energy, refractive_indices, interface_positions, roughnesses, resolution, num_points):
    """
    Compute the convolved reflection for a multilayer system with roughness.

    Parameters
    ----------
    incident_angles : numpy array
        Incident angles (in radians).
    energy : float
        Incident energy (eV).
    refractive_indices : numpy array of complex
        Refractive indices of the layers.
    interface_positions : numpy array of floats
        Positions of the interfaces (in meters).
    roughnesses : numpy array of floats
        Roughness of each interface (in meters).
    resolution : float
        Resolution of the incident beam (in radians).
    num_points : int
        Number of points to use in the convolution.

    Returns
    ----------
    yout : numpy array
        Convolved reflectivity.
    """
    
    # Calculate the wavevector k0 from the energy
    wavevector = 2 * np.pi * energy * scc.e / scc.h / scc.c
    
    dX = linspace(-resolution, resolution, num=num_points)
    yout = []
    mu = resolution / 2.35
    norm = nsum(exp(-(dX/mu)**2))
    yout = 0
    for delx in dX:
        _, R, _ = mlayer_rough(abs(incident_angles + delx), energy, refractive_indices, interface_positions, roughnesses)
        yout = yout + exp(-(delx/mu)**2) * abs(R[:, 0])**2 / norm
    return yout


def get_layers_info(energy, layers):
    """
    Process the layers and compute the refractive indices, thicknesses, and roughnesses.

    Parameters
    ----------
    energy : float
        Incident energy (eV).
    layers : array of layers 
        Each layer has a material (e.g., 'H2O'), density (g/cc), thickness, and roughness.

    Returns
    ----------
    refractive_indices : numpy array of complex
        Array of refractive indices for each layer.
    interface_positions : numpy array of floats
        Array of thicknesses for each layer (in meters).
    roughnesses : numpy array of floats
        Array of roughnesses for each layer (in meters).
    """
    num_layers = len(layers)
    refractive_indices = np.zeros(num_layers, complex)
    interface_positions = np.zeros(num_layers - 1)
    roughnesses = np.zeros(num_layers - 1)
    z = 0

    for i, (material, density, thickness, roughness) in enumerate(layers):
        delta, beta, _ = xdb.xray_delta_beta(material, density, energy)
        refractive_indices[i] = 1 - delta + 1j * beta
        if i > 0:
            interface_positions[i - 1] = z
            z -= thickness * scc.angstrom
            roughnesses[i - 1] = roughness * scc.angstrom

    return refractive_indices, interface_positions, roughnesses

def reflection_matrix(incident_angles, energy, layers):
    """
    Compute the reflection matrix based on the incident angles, energy, and layers.

    Parameters
    ----------
    incident_angles : numpy array float 
        Incident angles (in radians).
    energy : float
        Incident energy (eV).
    layers : array of layers 
        Each layer has a material (e.g., 'H2O'), density (g/cc), thickness, and roughness.

    Returns
    ----------
    T : numpy array (n_angles, n_layers)
        Transmission matrix returned by mlayer or mlayer_rough.
    R : numpy array (n_angles, n_layers)
        Reflectivity matrix returned by mlayer or mlayer_rough.
    kz : numpy array (n_angles, n_layers)
        Wavevector matrix returned by mlayer or mlayer_rough. (units of inverse meters)
    """
    refractive_indices, interface_positions, roughnesses = get_layers_info(energy, layers)
    T, R, kz = mlayer_rough(incident_angles, energy, refractive_indices, interface_positions, roughnesses)
    
    return T, R, kz, interface_positions


def standing_wave(heights, T, R, kz, interface_positions):
    """
    Calculate the electric field standing wave.
    
    Parameters
    ----------
    heights : numpy array (1d)
        Heights relative to the top surface at which to calculate
        the standing wave.
    T : numpy array (n_angles, n_layers)
        Transmission matrix returned by mlayer or mlayer_rough.
    R : numpy array (n_angles, n_layers)
        Reflectivity matrix returned by mlayer or mlayer_rough.
    kz : numpy array (n_angles, n_layers)
        Wavevector matrix returned by mlayer or mlayer_rough.
    interface_positions : numpy array (n_layers-1)
        Array of interface height positions.

    Returns
    -------
    I : numpy array (n_heights, n_angles)
        Standing wave intensity.
    E : numpy array (n_heights, n_angles)
        Electric field intensity.
    """
    num_angles, num_layers = np.shape(T)
    num_heights = len(heights)
    E = np.zeros((num_heights, num_angles), dtype=complex)
    
    for i in range(num_layers):
        if i == 0:
            wz = heights >= interface_positions[i]
        elif i == num_layers - 1:
            wz = heights < interface_positions[i-1]
        else:
            wz = (heights < interface_positions[i-1]) & (heights >= interface_positions[i])
        
        # Only calculate for the relevant subset of heights
        relevant_heights = heights[wz]
        num_relevant_heights = len(relevant_heights)
        T_full = np.broadcast_to(T[:, i], (num_relevant_heights, num_angles))
        R_full = np.broadcast_to(R[:, i], (num_relevant_heights, num_angles))
        kz_full = np.broadcast_to(kz[:, i], (num_relevant_heights, num_angles))
        z_full = np.transpose(np.broadcast_to(relevant_heights, (num_angles, num_relevant_heights)), (1, 0))
        
        E[wz, :] = np.exp(-1j * kz_full * z_full) * T_full
        E[wz, :] += np.exp(1j * kz_full * z_full) * R_full
    
    # Calculate the standing wave intensity
    I = np.abs(E)**2
    return I, E
