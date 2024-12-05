import torch
from torch import nn


def auto_pad(k, p=None, d=1):  # kernel, padding, dilation
	"""Pad to 'same' shape outputs."""
	if d > 1:
		k = d * (k - 1) + 1 if isinstance(k, int) else [d * (x - 1) + 1 for x in k]  # actual kernel-size
	if p is None:
		p = k // 2 if isinstance(k, int) else [x // 2 for x in k]  # auto-pad
	return p


class Conv(nn.Module):
	"""Standard convolution with args(ch_in, ch_out, kernel, stride, padding, groups, dilation, activation)."""
	
	default_act = nn.SiLU()  # default activation
	
	def __init__(self, c1, c2, k=1, s=1, p=None, g=1, d=1, act=True):
		"""Initialize Conv layer with given arguments including activation."""
		super().__init__()
		self.conv = nn.Conv2d(c1, c2, k, s, auto_pad(k, p, d), groups=g, dilation=d, bias=False)
		self.bn = nn.BatchNorm2d(c2)
		self.act = self.default_act if act is True else act if isinstance(act, nn.Module) else nn.Identity()
	
	def forward(self, x):
		"""Apply convolution, batch normalization and activation to input tensor."""
		return self.act(self.bn(self.conv(x)))
	
	def forward_fuse(self, x):
		"""Perform transposed convolution of 2D data."""
		return self.act(self.conv(x))


class WidthBlock(nn.Module):
	
	def __init__(self, c1, c2, kernel_sizes=(3, 5, 7)):
		super().__init__()
		self.convs = nn.ModuleList(
			[Conv(c1, c2, k) for k in kernel_sizes]
		)
		self.conv = nn.Conv2d(len(kernel_sizes) * c2, c2, kernel_size=1)
	
	def forward(self, x: torch.Tensor):
		x = torch.concatenate([conv(x) for conv in self.convs], dim=1)
		return self.conv(x)
