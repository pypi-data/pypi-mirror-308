#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2024/11/13 19:36
# @Author  : 兵
# @email    : 1747193328@qq.com


from NepTrain import utils

from ase.io import read as ase_read
from ase.io import write as ase_write
from .select import select_structures
from ..gpumd.plot import plot_md_selected
from ..nep.utils import read_symbols_from_file
from dscribe.descriptors import SOAP

def run_select(argparse):

    if utils.is_file_empty(argparse.trajectory_path):
        raise FileNotFoundError(f"传入了一个无效的文件路径：{argparse.trajectory_path}")
    utils.print_msg("正在读取文件，请稍等。。。")

    trajectory=ase_read(argparse.trajectory_path,":",format="extxyz")




    if utils.is_file_empty(argparse.base):
        base_train=[]
    else:
        base_train=ase_read(argparse.base,":",format="extxyz")
    if utils.is_file_empty(argparse.nep):
        utils.print_msg("传入无效的nep.txt路径，使用SOAP描述符")
        species=set()
        for atoms in trajectory+base_train:
            for i in atoms.get_chemical_symbols():
                species.add(i)

        species = list(species)
        r_cut = argparse.r_cut
        n_max = argparse.n_max
        l_max = argparse.l_max
        descriptor = SOAP(
            species=species,
            periodic=False,
            r_cut=r_cut,
            n_max=n_max,
            l_max=l_max,
        )

    else:
        descriptor=argparse.nep
    utils.print_msg("开始选点，请稍等。。。")

    selected_structures = select_structures(base_train,trajectory,descriptor,
                      max_selected=argparse.max_selected,
                      min_distance=argparse.min_distance,
                      )

    utils.print_msg(f"得到{len(selected_structures)}个结构" )

    ase_write(argparse.out_file_path, selected_structures)

    plot_md_selected(argparse.base,
                     argparse.trajectory_path,

                     argparse.out_file_path,
                     descriptor,
                       "./selected.png" ,

                     )
    utils.print_msg("选点分布图保存到./selected.png" )
    utils.print_msg(f"选取的结构保存到{argparse.out_file_path}" )

