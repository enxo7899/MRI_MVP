"""Inference Engines Package"""
from .totalsegmentator import TotalSegmentatorInfer
from .medsam import MedSAMInfer

__all__ = ["TotalSegmentatorInfer", "MedSAMInfer"]
