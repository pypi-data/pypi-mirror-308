import os
import math
import ezdxf
import pandas as pd
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import time
import datetime
import multiprocessing
from functools import partial
from shapely import Polygon, intersection, difference, MultiPolygon
import dask.dataframe as dd
import scipy.stats as ss
from multiprocessing import Pool
from marcobre.diff.backend.backend import create_historical_model,get_all_historical_model

plot_figures = False

#outfile = "stats_mb.xlsx"
#sheets = ['RPT_POLYGON_STATS', 'RPT_LT_BLOCK_MODEL', 'RPT_ST_BLOCK_MODEL']

heades_columns = {
  # 'RPT_POLYGON_STATS': ["POLYGON", "SG_CALC", "VOL_CALC", "N_VERTICES", "OTYPE_1", "VAR",]
  'RPT_POLYGON_STATS': ["MTYPE", "CUCN", "CATHM", "P", "S", "SG", "OTYPE", "STYPE", "ZVOL", "C", "AG", "MODLO", "BVU", "CUT", "FE", "FCUR", "CLASS", "FLMET", "AU", "CUAS", "BMU", "BENE", "LCUR", "LITH", "CUR", "TON", "RATOX", "PTOPO", "AS", "VERTICES", "UPDATE", "MODEL", "LEVEL"],

  
  'RPT_LT_BLOCK_MODEL': ["X", "Y", "Z", "LITH", "CUASD", "CUTD", "AU", "AG", "S", "CUCND", "CURD", "FE", "C", "SGF", "OTYPE", "PTOPO", "OXIDN", "CLASS", "FCURD", "LCUR", "FAGR", "FAUR", "FCCUD", "AREA", "LEASE", "MINED", "CUT", "CUAS", "CUCN", "CUR", "P", "AS", "ORECT", "OREPE", "BLKCT", "MODLO", "RATO", "CLOR", "AGMC", "AUMC", "CATHM", "FLMET", "GACM", "AUP", "CONCM", "CUASP", "CUTP", "GACP", "AGP", "FCUR", "FCCU", "OPXL", "OPXF", "BMU", "BVU", "BENE", "TPOX", "TPSUL", "TPDES", "DEST", "CATHD", "HIC", "HOROX", "HORSU", "HORAS", "PCPY", "FASCB", "MTYPE", "STYPE", "MC", "AUMET", "AGMET", "STOCK", "TBC", "CLCPT", "MIXTO", "CUTBC", "CUC", "CUM", "OVSA", "DOME", "AUPPM", "MCAF", "PF", "TON", "OTYPW", "SOLIF", "TOPOP", "SOL", "ZVOL", "MINER", "GBIN", "FASE", "SCD", "KTPD", "DIAS", "LITO", "RMZN", "RMZN%", "STZN", "STZN%", "WSZN", "WSZN%", "TCLS1", "TCLS2", "TCLS3", "OTYP1", "OTYP2", "OTYP3", "OTYP4", "ZVOL1", "ZVOL2", "ZVOL3", "XY", "SGTOP", "VOLUM", "LEAS2", "OTYLE", "PERIO", "F1", "F2", "F3", "P1", "P2", "P3", "COGOX", "COGSU", "FCUR2", "FLME2", "CONC2", "TPSU2", "HORA2", "FLMED", "CONCD", "DIF", "CLORO", "HUMED", "RATOX", "TONOP", "CPOXP", "CPOX", "CPSUP", "CPSU", "OVROP", "FASPE", "FASOL", "TOPO2", "TONO2", "FASP2", "CARAC", "CARBE", "CARSR", "F1CB", "F2CB", "F3CB", "P1CB", "P2CB", "P3CB", "SG", "FCAGD", "FCAG", "FCAUD", "FCAU", "DIFF", "DIFF2", "DIFF3", "ELEV.1", "PHASE", "LCUTR", "FAUR2", "FAGR2", "AUME2", "AGME2", "MCW", "MCS", "MCO", "DOME2", "AN1", "ROX2", "LCUR3", "UPDATE", "CORTE"],

  
  'RPT_ST_BLOCK_MODEL': ["X", "Y", "Z", "AREA", "CLASS", "OXIDN", "LITH", "CUT", "CUAS", "CUCN", "CUR", "C", "FE", "AG", "S", "AU", "AS", "P", "SGF", "MODLO", "BENCH", "PCTLK", "SG", "OTYPE", "ACT", "KFS", "IMIN1", "IMIN2", "IALT", "MIN1", "MIN2", "ALT", "ORECT", "RATIO", "LEASE", "STOCK", "TOPO", "ARS", "TON", "BENE", "BMU", "BVU", "XTRA1", "FLMET", "CONCM", "MAREA", "TPDES", "DEST", "GACM", "ESTIM", "MAT", "MTYPE", "STYPE", "ZVOL", "AGMC", "AUMC", "CATHM", "FCUR", "LCUR", "FAGR", "FAUR", "CATHD", "HORAS", "FCCU", "RATOX", "RATRE", "ACT2", "KFS2", "RMZN%", "ZMIN", "HPKT", "STZN%", "WSZN%", "CLOCM", "HUMCM", "STZN", "RMZN", "WSZN", "TROM", "HPKM3", "BMUSM", "BVUSM", "BENSM", "DESSM", "UPDATE", "CORTE"]
}

LARGO_PLAZO = "LARGO"
CORTO_PLAZO = "CORTO"

lp_batch_size = 2048 #4096

rot_angle = 330
ref_point = np.array([492300.0, 8320474.0])

cp_x_size = 4.5
cp_y_size = 4.5
cp_z_size = 12

lp_x_size = 18
lp_y_size = 18
lp_z_size = 12

#cpus = -1
cpus = max_cpus = multiprocessing.cpu_count()

variables = ["CLASS","LITH","CUT","CUAS","CUCN","CUR","C","FE","AG",
             "S","AU","P","AS","SG","OTYPE","MODLO","PTOPO","CATHM",
             "FLMET","FCUR","LCUR","BMU","BVU","BENE","MTYPE","STYPE","TON","ZVOL","RATOX"]

all_variables = variables + ["VERTICES", "MODEL", "UPDATE", "LEVEL"]

def extract_polygon_vertices(file):
    doc = ezdxf.readfile(file)

    # Access the modelspace
    msp = doc.modelspace()

    z_polygon = []
    polygon = []
    polygon_name = []
    # Iterate through entities in the modelspace
    for entity in msp:
        print(f"Entity Type: {entity.dxftype()}, Name: {entity.dxf.layer}")
        if entity.dxftype() == 'POLYLINE':
            # import pdb; pdb.set_trace()
            polyline = np.array([vertice.format('xyz') for vertice in entity.vertices]) # drop Z
            # import pdb; pdb.set_trace()
            xy_polyline = np.vstack((polyline[:, :2], polyline[0, :2]))
            z_polygon += polyline[:, 2].tolist()
        
        if entity.dxftype() == 'LWPOLYLINE':
            # import pdb; pdb.set_trace()
            xy_polyline = np.array(list(entity.vertices()))
            xy_polyline = np.vstack((xy_polyline, xy_polyline[0]))
            z_polygon.append(entity.dxf.elevation)

        polygon.append(xy_polyline)
        polygon_name.append(entity.dxf.layer)
        
    # import pdb; pdb.set_trace()
    z_polygon = np.round(np.array(z_polygon), 1)
    level = sp.stats.mode(z_polygon)
    # import pdb; pdb.set_trace()
    
    return polygon, z_polygon, level.mode, polygon_name


# In[21]:


def at_level(df, z_level, z_size):
    # is_at_level = [math.isclose(z - z_size/2, z_level) for z in df.Z]
    is_at_level = df.Z.apply(lambda z: math.isclose(z - z_size/2, z_level))
    return is_at_level



def rotateMatrix(a):
    return np.array([[np.cos(a), -np.sin(a)], [np.sin(a), np.cos(a)]])

# vertical to rotated system
def normal_system(df, ref_point, rot_angle):
    tmp_df = df.copy()
    xy = tmp_df[["X", "Y"]].to_numpy()

    arr = numpy_normal_system(xy, ref_point, rot_angle)

    tmp_df['X'] = arr[:, 0]
    tmp_df['Y'] = arr[:, 1]
    return tmp_df

def numpy_normal_system(xy, ref_point, rot_angle):
    rotation=-1*rot_angle
    orig_angle=360-rotation
    
    newxy = xy @ rotateMatrix(-orig_angle*np.pi/180).T
    arr=np.round(newxy,6)

    arr = arr + ref_point

    return arr

# rotated to vertical system
def vertical_system(df, ref_point, rot_angle):
    tmp_df = df.copy()
    xy = tmp_df[["X", "Y"]].to_numpy()
    rot_xy =  numpy_vertical_system(xy, ref_point, rot_angle)

    #import pdb; pdb.set_trace()
    tmp_df['X'] = rot_xy[:, 0]
    tmp_df['Y'] = rot_xy[:, 1]
    return tmp_df

def numpy_vertical_system(xy, ref_point, rot_angle):
    xy = xy - ref_point

    rotation=rot_angle
    orig_angle=-rotation
    
    newxy = xy @ rotateMatrix(-orig_angle*np.pi/180).T
    arr=np.round(newxy,6)

    return arr


# In[47]:

def vertices_block(row, x_size, y_size, z_size):
    #print(row)
    #dx, dy, dz = 1, 1, 1
    vertices = [
        (row.X - x_size/2, row.Y - y_size/2), # down left
        (row.X + x_size/2, row.Y - y_size/2), # down right
        (row.X + x_size/2, row.Y + y_size/2), # up right
        (row.X - x_size/2, row.Y + y_size/2), # up left
        
        (row.X - x_size/2, row.Y - y_size/2), # down left
    ]

    return vertices



# In[49]:

def clip_polygon(subject_polygon, clip_polygon, debug: bool = False):
    s = Polygon(subject_polygon)
    c = Polygon(clip_polygon)
    
    intersect = intersection(s, c)

    if isinstance(intersect, Polygon):
        vertices = list(intersect.exterior.coords)
        # import pdb; pdb.set_trace()
    else: # LineString
        if debug:
            import pdb; pdb.set_trace()
        vertices = None
    return vertices


# In[52]:


def vertices_to_string(vertices):
    pairs = []
    for x, y in vertices:
        pairs.append(f"{x},{y}")

    return ' '.join(pairs)


# In[55]:


def polygon_area(vertices):
    # shoelace formula
    area = 0.0

    n = len(vertices)
    for i in range(0,n):
        v0 = vertices[i]
        v1 = vertices[(i + 1) % n]
        
        x0, y0 = v0
        x1, y1 = v1
        
        area += (x0 + x1) * (y1 - y0)
     
    return abs(area / 2.0)

def polygon_vol(xy_vertices, height):
    base_area = polygon_area(xy_vertices)
    return height*base_area



# In[57]:

# def polygon_cut(df, polygon_list, debug: bool = False):
def polygon_cut(polygon_mb_df, pid, polyline, x_size, y_size, z_size, debug: bool = False):
    # mb_df["explored"] = False
    # mb_df["split"] = False

    # mb_df = df.copy()
    polygon_mb_df["polygon"] = -1
    # polygon_mb_df["id_block"] = polygon_mb_df.index
    vertices_block_udf =  partial(vertices_block, x_size=x_size, y_size=y_size, z_size=z_size)
    polygon_mb_df["vertices"] = polygon_mb_df.apply(vertices_block_udf, axis=1)

    block_polygon_vol = partial(polygon_vol,  height=z_size)

    polygon_blocks_list = []
    # n = len(polygon_list)-1
    # for pid, polyline in enumerate(polygon_list):
        # print(f"[{pid}/{n}]")
        
    polyline_vertices = polyline.tolist()
    for index, row in polygon_mb_df.iterrows():
        clipped_polygon = clip_polygon(subject_polygon=row.vertices, clip_polygon=polyline_vertices, debug=debug)

        if not clipped_polygon:
            continue

        # import pdb; pdb.set_trace()
        row["polygon"] = pid
        row["vertices"] = clipped_polygon
        row["VOL"] = block_polygon_vol(clipped_polygon)
        row["TON"] = row.VOL*row.SG
        polygon_blocks_list.append(row.to_dict())

        # mb_df.loc[index, "polygon"] = pid
        # mb_df.at[index, "vertices"] = clipped_polygon

            
    print(pid, len(polygon_blocks_list))
    #mb_df = mb_df[mb_df.polygon != -1]
    polygon_blocks_df = pd.DataFrame(polygon_blocks_list)
    return polygon_blocks_df

def polygon_cut_vector(arr):
    polygon_mb_df, pid, polyline, x_size, y_size, z_size = arr
    # print(pid)
    return polygon_cut(polygon_mb_df, pid, polyline, x_size, y_size, z_size)



# In[59]:


def block_partition(block_xyz, lp_x_size, lp_y_size, cp_x_size, cp_y_size, debug: bool = False):
    block_partition_coords = []
    x_steps = int(lp_x_size / cp_x_size)
    y_steps = int(lp_y_size / cp_y_size)
    sub_blocks_x = np.linspace(block_xyz[0] - (lp_x_size / 2) + (cp_x_size / 2), 
                               block_xyz[0] + (lp_x_size / 2) - (cp_x_size / 2), x_steps)
    sub_blocks_y = np.linspace(block_xyz[1] - (lp_y_size / 2) + (cp_y_size / 2), 
                               block_xyz[1] + (lp_y_size / 2) - (cp_y_size / 2), y_steps)

    # if sub_blocks_x.shape[0]*sub_blocks_y.shape[0] < 16:
    #     print(sub_blocks_x.shape, sub_blocks_y.shape)
    #     import pdb; pdb.set_trace()


    block_partition_coords = [(x, y) for x in sub_blocks_x for y in sub_blocks_y]

    block_partition_coords_arr = np.array(block_partition_coords)

    
    # import pdb; pdb.set_trace()
    return np.array(block_partition_coords)

def partition_lp_mb(lp_batch_df, lp_x_size, lp_y_size, lp_z_size, cp_x_size, cp_y_size, cp_z_size, debug: bool = False):
    block_partition_udf = partial(block_partition,
                                  lp_x_size=lp_x_size, lp_y_size=lp_y_size, 
                                  cp_x_size=cp_x_size, cp_y_size=cp_y_size)
    xy_lp_batch = lp_batch_df[['X', 'Y']]
    lp_partition_batch = np.apply_along_axis(block_partition_udf, axis=1, arr=xy_lp_batch)
    
    lp_partition_list = []
    #idx_offset = lp_batch_df.index[0]
    for idx, batch_partition_coords in enumerate(lp_partition_batch):
        block = lp_batch_df.iloc[idx]
        
        partition_block = block.copy()
        for block_partition_coords in batch_partition_coords:
            # print(idx, block_partition_coords)
            partition_block["X"] = block_partition_coords[0]
            partition_block["Y"] = block_partition_coords[1]
            # import pdb; pdb.set_trace()
            lp_partition_list.append(partition_block.to_dict())

    lp_partition_df = pd.DataFrame(lp_partition_list)
    
    # if debug:
    #     plt.figure(figsize=(20,20))
    #     plt.scatter(lp_partition_df.X, lp_partition_df.Y, label=f"batch-{lp_batch_df.index[0]}")
    #     plt.legend()
    #     plt.show()
        
    return lp_partition_df


def partition_lp_mb_vector(arr):
    lp_batch_df, lp_x_size, lp_y_size, lp_z_size, cp_x_size, cp_y_size, cp_z_size = arr
    # import pdb; pdb.set_trace()
    print(lp_batch_df.index[0])
    return partition_lp_mb(lp_batch_df, lp_x_size, lp_y_size, lp_z_size, cp_x_size, cp_y_size, cp_z_size)


# ### Data Partition

# In[61]:


def pairwise(iterable):
    # pairwise('ABCDEFG') → AB BC CD DE EF FG

    iterator = iter(iterable)
    a = next(iterator, None)

    for b in iterator:
        yield a, b
        a = b


# In[85]:


def parallel_polygon_cut(partition_mb_df, polygon_list, x_size, y_size, z_size, debug: bool = False):
    polygon_batches = []

    for pid, polyline in enumerate(polygon_list):
        polyline_min = polyline.min(axis=0) - np.array([x_size, y_size])
        polyline_max = polyline.max(axis=0) + np.array([x_size, y_size])
    
        batch_polygon_mb_df = partition_mb_df[((partition_mb_df.X >= polyline_min[0]) & (partition_mb_df.Y >= polyline_min[1])) & 
                                                ((partition_mb_df.X <= polyline_max[0]) & (partition_mb_df.Y <= polyline_max[1]))]

        print(pid, batch_polygon_mb_df.shape)
        if debug:
            plt.figure(figsize=(20,20))
            plt.scatter(partition_mb_df.X, partition_mb_df.Y, label="blocks")
            # import pdb; pdb.set_trace()
            plt.scatter([polyline_min[0], polyline_max[0]], [polyline_min[1], polyline_max[1]], label="polyline")
            plt.legend()
            plt.show()
            import pdb; pdb.set_trace()
        polygon_batches.append([batch_polygon_mb_df, pid, polyline, x_size, y_size, z_size])
    

    pool = Pool(processes=cpus)
    
    partition_mb_pool = pool.map(polygon_cut_vector, polygon_batches)
    polygon_cut_df = pd.concat(partition_mb_pool, ignore_index=True)

    return polygon_cut_df


# In[86]:


# def plot_polygon_cut(polygon_df, polygon_list):
    plt.figure(figsize=(20,20))
    for pid, polyline in enumerate(polygon_list):
        # plt.scatter(cp_df.X, cp_df.Y, label="blocks")
        
        tmp_df = polygon_df[polygon_df.polygon == pid]
        print(pid, tmp_df.shape)
        #import pdb; pdb.set_trace()
        vertices_arr = None
        for vertices in tmp_df.vertices:
            if vertices_arr is None:
                vertices_arr = np.array(vertices)
            else:
                vertices_arr = np.vstack((vertices_arr, np.array(vertices)))
    
        
        plt.scatter(vertices_arr[:, 0], vertices_arr[:, 1], label=f"blocks (polygon={polygon_name[pid]})")
        plt.scatter(polyline[:, 0], polyline[:, 1], label=f"polygon={polygon_name[pid]}")
        plt.legend()
        plt.plot()
        plt.show()


# def plot_each_polygon_cut(polygon_df, polygon_list):
    for pid, polyline in enumerate(polygon_list):
        plt.figure(figsize=(20,20))
        # plt.scatter(cp_df.X, cp_df.Y, label="blocks")
        
        tmp_df = polygon_df[polygon_df.polygon == pid]
        print(pid, tmp_df.shape)
        #import pdb; pdb.set_trace()
        vertices_arr = None
        for vertices in tmp_df.vertices:
            if vertices_arr is None:
                vertices_arr = np.array(vertices)
            else:
                vertices_arr = np.vstack((vertices_arr, np.array(vertices)))
    
        
        plt.scatter(vertices_arr[:, 0], vertices_arr[:, 1], label=f"blocks (polygon={polygon_name[pid]})")
        plt.scatter(polyline[:, 0], polyline[:, 1], label=f"polygon={polygon_name[pid]}")
        plt.legend()
        plt.plot()
        plt.show()


# In[94]:


def polygon_otype_stats(group):
    local_vars = list(set(variables).intersection(group.columns))
    
    stats = group[local_vars].describe()


    weighted_avg = {}

    for var in local_vars:
        weighted_avg[var] = np.average(group[var].values, weights=group.TON.values) #sum(group[var]*group.TON)/group.TON.sum()

    mode = {}
    for var in local_vars:
        # import pdb; pdb.set_trace()
        mode[var] = ss.mode(group[var].values).mode

    extra_stats = [
        pd.DataFrame(group[local_vars].sum().to_dict(), index=['sum']),
        pd.DataFrame(mode, index=['mode']),
        pd.DataFrame(weighted_avg, index=['weighted_avg'])
    ]
    
    all_stats = pd.concat([stats, *extra_stats])
    # import pdb; pdb.set_trace()
    
    # import pdb; pdb.set_trace()
    return all_stats

def polygon_stats(group):
    local_vars = list(set(variables).intersection(group.columns))
    stats = group[local_vars].describe()
    # import pdb; pdb.set_trace()

    weighted_avg = {}
    for var in local_vars:
        weighted_avg[var] = np.average(group[var].values, weights=group.TON.values) #sum(group[var]*group.TON)/group.TON.sum()

    mode = {}
    for var in local_vars:
        # import pdb; pdb.set_trace()
        mode[var] = ss.mode(group[var].values).mode
    
    extra_stats = [
        # pd.DataFrame(polygon_group.TON.sum().to_dict(), index=['TON']),
        pd.DataFrame(group[local_vars].sum().to_dict(), index=['sum']),
        pd.DataFrame(mode, index=['mode']),
        pd.DataFrame(weighted_avg, index=['weighted_avg'])
    ]

    all_stats = pd.concat([stats, *extra_stats])

    return all_stats

def stats_by_polygon(mb_polygon_df, z_size):
    # df = mb_polygon_df.copy()

    block_polygon_vol = partial(polygon_vol,  height=z_size)
    #import pdb; pdb.set_trace()
    mb_polygon_df["VOL"] = mb_polygon_df.vertices.apply(block_polygon_vol)
    mb_polygon_df["TON"] = mb_polygon_df.SG*mb_polygon_df.VOL

    polygon_stats_df = mb_polygon_df.groupby(by=['polygon']).apply(polygon_stats)
    polygon_otype_stats_df = mb_polygon_df.groupby(by=['polygon', 'OTYPE']).apply(polygon_otype_stats)
    
    return polygon_stats_df, polygon_otype_stats_df


# In[95]:


def generete_otype_index(stats_df, polygon_df, polygon_name, polygon_list, z_size):
    new_index = []

    n_vertices = {}
    sg = {}
    vol = {}
    # z_size = 12
    for pid, var in stats_df.index:
        if pid not in n_vertices:
            n_vertices[pid] = len(polygon_list[pid].tolist())

        if pid not in vol:
            vol[pid] = polygon_area(polygon_list[pid].tolist())*z_size

        if pid not in sg:
            polygon_idx = [polygon == pid for polygon in polygon_df.polygon]
            sg[pid] = polygon_df.loc[polygon_idx].TON.sum()/vol[pid]
            # print(f"{'='*10} {polygon_name[pid]} {'='*10}")
            # print(sg[pid],vol[pid])
            # print(polygon_df.loc[polygon_idx].SG.mean(), polygon_df.loc[polygon_idx].TON.sum())
            # import pdb; pdb.set_trace()
        # if pid not in ton_polygon:
        #     ton_polygon[pid] = lp_polygon_df[lp_polygon_df.polygon == pid].TON.sum()

        #  df[df.polygon == pid].TON.sum()
        new_index.append((polygon_name[pid], sg[pid], vol[pid], n_vertices[pid], None, var))
        #new_index.append((polygon_name[pid], None, var))
            
    new_index = pd.MultiIndex.from_tuples(new_index, names=["POLYGON", "SG_CALC", "VOL_CALC", "N_VERTICES", "OTYPE_1", "VAR"])
    #new_index = pd.MultiIndex.from_tuples(new_index, names=["polygon", "OTYPE", "var"])
    return new_index


# In[96]:


def resolve_polygon_name_index(stats_df, polygon_df, polygon_name, polygon_list, z_size):
    new_index = []

    n_vertices = {}
    sg = {}
    vol = {}
    # z_size = 12
    for pid, otype, var in stats_df.index:
        if pid not in n_vertices:
            n_vertices[pid] = len(polygon_list[pid].tolist())

        if pid not in vol:
            vol[pid] = polygon_area(polygon_list[pid].tolist())*z_size
        
        if pid not in sg:
            # import pdb; pdb.set_trace()
            polygon_idx = [polygon == pid for polygon in polygon_df.polygon]
            sg[pid] = polygon_df.loc[polygon_idx].TON.sum()/vol[pid]
            
            # print(sg[pid],vol[pid], vol[pid]*sg[pid])
            # print(polygon_df.loc[polygon_idx].SG.mean(), polygon_df.loc[polygon_idx].VOL.sum(), polygon_df.loc[polygon_idx].TON.sum())
            # import pdb; pdb.set_trace()
            #import pdb; pdb.set_trace()
        # if pid not in ton_polygon:
        #     ton_polygon[pid] = lp_polygon_df[lp_polygon_df.polygon == pid].TON.sum()
    
        new_index.append((polygon_name[pid], sg[pid], vol[pid], n_vertices[pid], otype, var))
        #new_index.append((polygon_name[pid], otype, var))
            
    new_index = pd.MultiIndex.from_tuples(new_index, names=["POLYGON", "SG_CALC", "VOL_CALC", "N_VERTICES", "OTYPE_1", "VAR"])
    #new_index = pd.MultiIndex.from_tuples(new_index, names=["polygon", "OTYPE", "var"])
    return new_index


# In[97]:


# lp_polygon_df.polygon.unique(), lp_polygon_df.OTYPE.unique()


# In[99]:


def get_new_variables(df, new_vars):
    diff_vars = set(new_vars).difference(set(df.columns))
    return list(diff_vars)
# new_variables = set(variables).difference(set(lp_polygon_otype_stats_df.columns))

 # In[108]:

def rotate_and_format_vertices(df):
    # import pdb; pdb.set_trace()
    #df["CORTE"] = df.polygon.map(rename_polygon_map)
    
    #tmp_df_rot = normal_system(tmp_df, ref_point, rot_angle)
    
    for idx, polygon_vertices in df.VERTICES.items():
        # import pdb; pdb.set_trace()
        polygon_vertices_rot = numpy_normal_system(np.array(polygon_vertices), ref_point, rot_angle)
        polygon_vertices_rot_list = polygon_vertices_rot.tolist()
        # tmp_df.at[idx, "vertices"] = polygon_vertices_rot_list
        df.at[idx, "VERTICES"] = vertices_to_string(polygon_vertices_rot_list)

    return df

def format_header(df, headers):
    for var in headers:
      if var not in df.columns:
          df[var] = np.nan
    
    # tmp_df.to_csv(output, index=False)
    return df[headers]

def algorithm_function_models(long_term_model,short_term_model,cuttings):
    #cpus=-1
    global_start_time = time.time()
    lp_df_rot = dd.read_csv(long_term_model, compression='zip')
    lp_df_rot["id_block"] = lp_df_rot.index
    lp_df_rot = lp_df_rot.rename(columns={'EAST': 'X', 'NORTH': 'Y', 'ELEV': 'Z'})

    cp_df_rot = dd.read_csv(short_term_model)
    cp_df_rot["id_block"] = cp_df_rot.index
    cp_df_rot = cp_df_rot.rename(columns={'EAST': 'X', 'NORTH': 'Y', 'ELEV': 'Z'})
    polygon_file = cuttings

    polygon_list_rot, z_polygon, level, polygon_name = extract_polygon_vertices(polygon_file)

    lp_df_rot = lp_df_rot[at_level(lp_df_rot, level, z_size=lp_z_size)].compute()
    lp_df_rot.reset_index(inplace=True)
    lp_df_rot["id_block"] = lp_df_rot.index

    cp_df_rot = cp_df_rot[at_level(cp_df_rot, level, z_size=cp_z_size)].compute()
    cp_df_rot.reset_index(inplace=True)
    cp_df_rot["id_block"] = cp_df_rot.index

    lp_df = vertical_system(lp_df_rot, ref_point, rot_angle)
    cp_df = vertical_system(cp_df_rot, ref_point, rot_angle)
    polygon_list = [numpy_vertical_system(polygon_rot, ref_point, rot_angle) for polygon_rot in polygon_list_rot]

    if plot_figures:
        plt.figure(figsize=(20,20))
        plt.scatter(lp_df.X, lp_df.Y, label="blocks (lp)")
        plt.scatter(cp_df.X, cp_df.Y, label="blocks (cp)")
        for pid, polygon in enumerate(polygon_list):
            plt.scatter(polygon[:, 0], polygon[:, 1], label=f"polygon-{pid}")
        plt.legend()
        plt.show()

    batch_idx = np.arange(0, lp_df.shape[0]+lp_batch_size, lp_batch_size)

    lp_mb_batches = []

    max_lp_df_idx = lp_df.shape[0]
    for start_idx, end_idx in pairwise(batch_idx):
        if end_idx > max_lp_df_idx:
            end_idx = max_lp_df_idx
            
        lp_batch_df = lp_df.iloc[start_idx:end_idx]
        print(start_idx, end_idx, lp_batch_df.index)
        # import pdb; pdb.set_trace()
        lp_batch_df_copy = lp_batch_df.copy()
        lp_mb_batches.append([lp_batch_df_copy, lp_x_size, lp_y_size, lp_z_size, cp_x_size, cp_y_size, cp_z_size])
    
    #cpus = max_cpus = multiprocessing.cpu_count()
    #max_cpus = multiprocessing.cpu_count()
    #cpus = max_cpus if cpus > max_cpus or cpus <= 0 else cpus
    partition_start_time = time.time()
    print(cpus, max_cpus, "debug numero de cpus")
    pool = Pool(processes=cpus)
    lp_mb_partition_pool = pool.map(partition_lp_mb_vector, lp_mb_batches)

    lp_partition_df = pd.concat(lp_mb_partition_pool, ignore_index=True)
    partition_elapsed_time = time.time() - partition_start_time

    lp_polygon_df = parallel_polygon_cut(lp_partition_df, polygon_list, x_size=cp_x_size, y_size=cp_y_size, z_size=cp_z_size)

    # if plot_figures:
    #     plot_polygon_cut(lp_polygon_df, polygon_list)

    # if plot_figures:
    #     plot_each_polygon_cut(lp_polygon_df, polygon_list)
    
    cp_polygon_df = parallel_polygon_cut(cp_df, polygon_list, 
                                        x_size=cp_x_size, y_size=cp_y_size, z_size=cp_z_size)
    
    # if plot_figures:
    #     plot_polygon_cut(cp_polygon_df, polygon_list)

    # if plot_figures:
    #     plot_each_polygon_cut(cp_polygon_df, polygon_list)
    
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    rename_polygon_map = {idx: name for idx, name in enumerate(polygon_name)}


    # import pdb; pdb.set_trace()
    cp_polygon_df["UPDATE"] = now
    cp_polygon_df["CORTE"] = cp_polygon_df.polygon.map(rename_polygon_map)
    
    lp_polygon_df["UPDATE"] = now
    lp_polygon_df["CORTE"] = lp_polygon_df.polygon.map(rename_polygon_map)

    lp_polygon_stats_df, lp_polygon_otype_stats_df = stats_by_polygon(lp_polygon_df, z_size=lp_z_size)
    lp_polygon_otype_stats_df["VERTICES"] = [vertices_to_string(polygon_list_rot[idx].tolist()) for idx, *_ in lp_polygon_otype_stats_df.index]
    lp_polygon_otype_stats_df["UPDATE"] = now
    lp_polygon_otype_stats_df["MODEL"] = LARGO_PLAZO
    lp_polygon_otype_stats_df["LEVEL"] = level

    if new_variables := get_new_variables(lp_polygon_otype_stats_df, all_variables):
        print(new_variables)
        lp_polygon_otype_stats_df[new_variables] = None

    new_index = resolve_polygon_name_index(lp_polygon_otype_stats_df, lp_polygon_df, polygon_name, polygon_list, z_size=lp_z_size)

    lp_polygon_otype_stats_df_formatted = pd.DataFrame(lp_polygon_otype_stats_df.values, 
                                                    index=new_index, columns=lp_polygon_otype_stats_df.columns)

    # lp_polygon_stats_df["VERTICES"] = [polygon_list_rot[idx] for idx, *_ in lp_polygon_stats_df.index]
    lp_polygon_stats_df["VERTICES"] = [vertices_to_string(polygon_list_rot[idx].tolist()) for idx, *_ in lp_polygon_stats_df.index]
    lp_polygon_stats_df["UPDATE"] = now
    lp_polygon_stats_df["MODEL"] = LARGO_PLAZO 
    lp_polygon_stats_df["LEVEL"] = level

    if new_variables := get_new_variables(lp_polygon_stats_df, all_variables):
        print(new_variables)
        lp_polygon_stats_df[new_variables] = np.nan

    print(lp_polygon_stats_df.columns)
    new_index = generete_otype_index(lp_polygon_stats_df, lp_polygon_df, polygon_name, polygon_list, z_size=lp_z_size)
    lp_polygon_stats_df_formatted = pd.DataFrame(lp_polygon_stats_df.values, index=new_index, columns=lp_polygon_stats_df.columns)

    cp_polygon_stats_df, cp_polygon_otype_stats_df = stats_by_polygon(cp_polygon_df, z_size=cp_z_size)

    # cp_polygon_otype_stats_df["VERTICES"] = [polygon_list_rot[idx] for idx, *_ in cp_polygon_otype_stats_df.index]
    cp_polygon_otype_stats_df["VERTICES"] = [vertices_to_string(polygon_list_rot[idx].tolist()) for idx, *_ in cp_polygon_otype_stats_df.index]
    cp_polygon_otype_stats_df["UPDATE"] = now
    cp_polygon_otype_stats_df["MODEL"] = CORTO_PLAZO
    cp_polygon_otype_stats_df["LEVEL"] = level

    if new_variables := get_new_variables(cp_polygon_otype_stats_df, all_variables):
        print(new_variables)
        cp_polygon_otype_stats_df[new_variables] = np.nan


    print(cp_polygon_otype_stats_df.columns)
    new_index = resolve_polygon_name_index(cp_polygon_otype_stats_df, cp_polygon_df, polygon_name, polygon_list, z_size=cp_z_size)

    cp_polygon_otype_stats_df_formatted = pd.DataFrame(cp_polygon_otype_stats_df.values, 
                                                    index=new_index, columns=cp_polygon_otype_stats_df.columns)

    # cp_polygon_stats_df["VERTICES"] = [polygon_list_rot[idx] for idx, *_ in cp_polygon_stats_df.index]
    cp_polygon_stats_df["VERTICES"] = [vertices_to_string(polygon_list_rot[idx].tolist()) for idx, *_ in cp_polygon_stats_df.index]
    cp_polygon_stats_df["UPDATE"] = now
    cp_polygon_stats_df["MODEL"] = CORTO_PLAZO
    cp_polygon_stats_df["LEVEL"] = level

    if new_variables := get_new_variables(cp_polygon_stats_df, all_variables):
        print(new_variables)
        cp_polygon_stats_df[new_variables] = np.nan


    print(cp_polygon_stats_df.columns)
    new_index = generete_otype_index(cp_polygon_stats_df, cp_polygon_df, polygon_name, polygon_list, z_size=cp_z_size)
    cp_polygon_stats_df_formatted = pd.DataFrame(cp_polygon_stats_df.values, index=new_index, columns=cp_polygon_stats_df.columns)

    
    polygon_stats_df = pd.concat([
        lp_polygon_otype_stats_df_formatted,
        lp_polygon_stats_df_formatted, 
        cp_polygon_otype_stats_df_formatted,     
        cp_polygon_stats_df_formatted
    ])


    #! Create file
    #! Current Date and hour
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    #! Define the directory to save the output
    user_home = os.path.expanduser("~")
    output_dir = os.path.join(user_home, 'ComparaciónDeModelos')

    # Create the directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    now = datetime.datetime.now().strftime("_%Y-%m-%d_%H-%M")
    #!#######################
    outfile = "stats_mb" + now + ".xlsx"
    final_output = os.path.join(output_dir,outfile)

    # Write output to excel sheets
    # Write output to excel sheets
    print(f"output: {final_output}")
    with pd.ExcelWriter(final_output) as writer:
      sheets = {'RPT_POLYGON_STATS': polygon_stats_df, 'RPT_LT_BLOCK_MODEL': lp_polygon_df, 'RPT_ST_BLOCK_MODEL': cp_polygon_df}

      for sheet_name, sheet_data in sheets.items():
        print(f"Writing '{sheet_name}' sheet")
        
        sheet_data_formated = format_header(sheet_data, heades_columns[sheet_name])

        if sheet_name == 'RPT_POLYGON_STATS':
          index_values = sheet_data_formated.index.values
          index_values = np.array(index_values.tolist())
          index_columns = sheet_data_formated.index.names

          values = sheet_data_formated.values
          columns = sheet_data_formated.columns

          # print(index_values.shape, values.shape)
          #import pdb; pdb.set_trace()
          index_values[:, 1:-1] = np.round(index_values[:, 1:-1].astype(np.float64), decimals=6)
          #index_values = np.round(index_values, decimals=6)
          values = np.hstack((index_values, values))
          #values = np.round(values, decimals=6)
          sheet_data_formated = pd.DataFrame(values, columns=list(index_columns) + list(columns))  
          # sheet_data = rotate_and_format_vertices(sheet_data)
        
        sheet_data_formated_round = sheet_data_formated.round(decimals=6)
        #import pdb; pdb.set_trace()
        sheet_data_formated_round.to_excel(writer, sheet_name=sheet_name, index=False)
        # Open the output directory
        # save in DB
        create_historical_model(f"{long_term_model}",f"{short_term_model}",f"{cuttings}",f"stats_mb_{current_datetime}.xlsx")
        historical_records = get_all_historical_model()
        print(historical_records)

    if os.name == 'nt':  # For Windows
        os.startfile(output_dir)
    elif os.name == 'posix':  # For macOS/Linux
        subprocess.run(['open', output_dir])  # macOS  
    global_elapsed_time = time.time() - global_start_time 
    # global_elapsed_time/60

    #lp_mb_file = pd.read_csv(long_term_model, compression='zip')
    #cp_mb_file = pd.read_csv(short_term_model)
    

    # #! Create file
    # #! Current Date and hour
    # current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    # #! Define the directory to save the output
    # user_home = os.path.expanduser("~")
    # output_dir = os.path.join(user_home, 'ComparaciónDeModelos')

    # # Create the directory if it doesn't exist
    # os.makedirs(output_dir, exist_ok=True)
    # #!#######################

    # lp_df_rot.rename(columns={'EAST': 'X', 'NORTH': 'Y', 'ELEV': 'Z'},inplace=True)
    # cp_df_rot.rename(columns={'EAST': 'X', 'NORTH': 'Y', 'ELEV': 'Z'},inplace=True)

    # polygon_list_rot, z_polygon, level, polygon_name = extract_polygon_vertices(polygon_file)

    # lp_df_rot = lp_df_rot[at_level(lp_df_rot, level, z_size=lp_z_size)]
    # cp_df_rot = cp_df_rot[at_level(cp_df_rot, level, z_size=cp_z_size)]
    # lp_df = vertical_system(lp_df_rot, ref_point, rot_angle)
    # cp_df = vertical_system(cp_df_rot, ref_point, rot_angle)
    # polygon_list = [numpy_vertical_system(polyline, ref_point, rot_angle) for polyline in polygon_list_rot]
    # lp_polygon_df = polygon_cut(lp_df, polygon_list, x_size=lp_x_size, y_size=lp_y_size, z_size=lp_z_size)
    # cp_polygon_df = polygon_cut(cp_df, polygon_list,  x_size=cp_x_size, y_size=cp_y_size, z_size=cp_z_size)

    # all_variables = variables + ["VERTICES", "MODEL", "DATE", "LEVEL"]

    # now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # rename_polygon_map = {idx: name for idx, name in enumerate(polygon_name)}

    # #!Largo Plazo

    # lp_polygon_stats_df, lp_polygon_otype_stats_df = stats_by_polygon(lp_polygon_df, z_size=lp_z_size)

    # def write_blocks_to_file(df, output):
    #     tmp_df = df.copy()
    #     tmp_df.polygon = tmp_df.polygon.map(rename_polygon_map)
        
    #     #tmp_df_rot = normal_system(tmp_df, ref_point, rot_angle)
        
    #     for idx, polygon_vertices in tmp_df.vertices.items():
    #         # import pdb; pdb.set_trace()
    #         polygon_vertices_rot = numpy_normal_system(np.array(polygon_vertices), ref_point, rot_angle)
    #         polygon_vertices_rot_list = polygon_vertices_rot.tolist()
    #         tmp_df.at[idx, "vertices"] = polygon_vertices_rot_list
            
    #         centroid = find_centroid(polygon_vertices_rot_list)
    #         if centroid is None:
    #             xy = tmp_df[["X", "Y"]].values
    #             xy_rot = numpy_normal_system(xy, ref_point, rot_angle)
    #             tmp_df.X = xy_rot[:, 0]
    #             tmp_df.Y = xy_rot[:, 1]
    #         else:
    #             tmp_df.loc[idx, "X"] = centroid[0]
    #             tmp_df.loc[idx, "Y"] = centroid[1]
    #         # print(idx, polygon_vertices)
        
    #     tmp_df.to_csv(output, index=False)
    #     return tmp_df
    
    # #*Salida Largo plazo Csv
    # #output = f"{os.path.splitext(long_term_model)[0]}-BLOCKS.csv"
    # output = f"General_OCModel_1-BLOCKS_{current_datetime}.csv"
    # output_path_long = os.path.join(output_dir, output)
    # lp_polygon_df_blocks = write_blocks_to_file(lp_polygon_df, output_path_long)
    # #####

    # lp_polygon_otype_stats_df["VERTICES"] = [polygon_list_rot[idx] for idx, *_ in lp_polygon_otype_stats_df.index]
    # lp_polygon_otype_stats_df["DATE"] = now
    # lp_polygon_otype_stats_df["MODEL"] = LARGO_PLAZO
    # lp_polygon_otype_stats_df["LEVEL"] = level

    # if new_variables := get_new_variables(lp_polygon_otype_stats_df, all_variables):
    #     print(new_variables)
    #     lp_polygon_otype_stats_df[new_variables] = None
    
    # new_index = resolve_polygon_name_index(lp_polygon_otype_stats_df, lp_polygon_df, polygon_name, polygon_list, z_size=lp_z_size)
    # lp_polygon_otype_stats_df_formatted = pd.DataFrame(lp_polygon_otype_stats_df.values, 
    #                                                index=new_index, columns=lp_polygon_otype_stats_df.columns)


    # #Polygon stats

    # lp_polygon_stats_df["VERTICES"] = [polygon_list_rot[idx] for idx, *_ in lp_polygon_stats_df.index]
    # lp_polygon_stats_df["DATE"] = now
    # lp_polygon_stats_df["MODEL"] = LARGO_PLAZO 
    # lp_polygon_stats_df["LEVEL"] = level

    # if new_variables := get_new_variables(lp_polygon_stats_df, all_variables):
    #     print(new_variables)
    #     lp_polygon_stats_df[new_variables] = np.nan

    # new_index = generete_otype_index(lp_polygon_stats_df, lp_polygon_df, polygon_name, polygon_list, z_size=lp_z_size)
    # lp_polygon_stats_df_formatted = pd.DataFrame(lp_polygon_stats_df.values, index=new_index, columns=lp_polygon_stats_df.columns)


    # #!Corto Plazo

    # cp_polygon_stats_df, cp_polygon_otype_stats_df = stats_by_polygon(cp_polygon_df, z_size=cp_z_size)

    # #output = f"{os.path.splitext(short_term_model)[0]}-BLOCKS.csv"
    # output = f"lp-BLOCKS_{current_datetime}.csv"
    # output_path_short = os.path.join(output_dir, output)
    # cp_polygon_df_blocks = write_blocks_to_file(cp_polygon_df, output_path_short)

    # #*otype stats

    # cp_polygon_otype_stats_df["VERTICES"] = [polygon_list_rot[idx] for idx, *_ in cp_polygon_otype_stats_df.index]
    # cp_polygon_otype_stats_df["DATE"] = now
    # cp_polygon_otype_stats_df["MODEL"] = CORTO_PLAZO
    # cp_polygon_otype_stats_df["LEVEL"] = level

    # if new_variables := get_new_variables(cp_polygon_otype_stats_df, all_variables):
    #     print(new_variables)
    #     cp_polygon_otype_stats_df[new_variables] = np.nan
    
    # new_index = resolve_polygon_name_index(cp_polygon_otype_stats_df, cp_polygon_df, polygon_name, polygon_list, z_size=cp_z_size)
    # cp_polygon_otype_stats_df_formatted = pd.DataFrame(cp_polygon_otype_stats_df.values,index=new_index, columns=cp_polygon_otype_stats_df.columns)

    # #*polygon stats

    # cp_polygon_stats_df["VERTICES"] = [polygon_list_rot[idx] for idx, *_ in cp_polygon_stats_df.index]
    # cp_polygon_stats_df["DATE"] = now
    # cp_polygon_stats_df["MODEL"] = CORTO_PLAZO
    # cp_polygon_stats_df["LEVEL"] = level

    # if new_variables := get_new_variables(cp_polygon_stats_df, all_variables):
    #     print(new_variables)
    #     cp_polygon_stats_df[new_variables] = np.nan

    # new_index = generete_otype_index(cp_polygon_stats_df, cp_polygon_df, polygon_name, polygon_list, z_size=cp_z_size)
    # cp_polygon_stats_df_formatted = pd.DataFrame(cp_polygon_stats_df.values, index=new_index, columns=cp_polygon_stats_df.columns)

    # polygon_stats_df = pd.concat([
    # lp_polygon_otype_stats_df_formatted,
    # lp_polygon_stats_df_formatted, 
    # cp_polygon_otype_stats_df_formatted,     
    # cp_polygon_stats_df_formatted
    # ])

    # #*Salida polygon-stats.csv
    # output = f"POLYGON-STATS_{current_datetime}.csv"
    # #polygon_stats_df.to_csv(output)
    # #polygon_stats_df.MODEL.unique()


    # #Create file
    # output_path = os.path.join(output_dir, output)
    # polygon_stats_df.to_csv(output_path)