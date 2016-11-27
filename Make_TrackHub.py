import os
import argparse
import sys



def main():
	args=get_args()

	if len(sys.argv)<2:
		print('Abort! You do not have any parameter input, please check your input!')
	else:
		# for i in range(len(sys.argv)):
		# 	print(len(sys.argv),sys.argv[i])
		run_process(args)



def check_main_parameters(parameter_names):
	print('Abort! No '+parameter_names+' and please check again!')
	return False

def check_optional_parameters(parameters,parameter_names):
	if parameters=='none':
		print('Attention! No '+parameter_names+' !')
		return True

# def get_absolute_path():
# 	path=os.getcwd()
# 	return path

def get_files(input_path):
	abs_input_path=os.path.abspath(input_path)
	if os.path.isdir(abs_input_path):
		final_bigfiles=[]
		files=os.listdir(abs_input_path)
		for line in files:
			if line.endswith('.bigWig') | line.endswith('.bw') | line.endswith('.bigBed'):
				final_bigfiles.append(line)
			else:
				pass

		if len(final_bigfiles)==0:
			print(abs_input_path+'does not exists any bigBed or bigWig files! Please check your folder again!')
		else:
			return final_bigfiles
	else:
		print('Abort! '+abs_input_path+' is not a avaiable folder, please check again!')



def make_dir(foldername):
	if not os.path.exists(foldername):
		os.mkdir(foldername)
		return foldername
	else: 
		return foldername




def get_args():

	parser = argparse.ArgumentParser()

	parser.add_argument('-i', '--input', help='input folder. (eg: /home/a)', default='none')
	parser.add_argument('-G', '--genomes', help='genome name. (eg: mm10)', default='none')
	parser.add_argument('-H', '--hub', help='hub name. (eg: my_sample)', default='none')
	parser.add_argument('-O', '--output', help='output directory. (eg: my_output/)', default='none')
	parser.add_argument('-E', '--email', help='user email.', default='none')
	args = parser.parse_args()

	return args



def check_before_run(args):
	if args.input=='none':
		check_main_parameters('-i/--input')
		return False
	elif args.genomes=='none':
		check_main_parameters('-G/--genomes')
		return False
	elif args.hub=='none':
		check_main_parameters('-H/--hub')
		return False
	elif args.output=='none':
		check_main_parameters('-O/--output')
		return False
	else:
		check_optional_parameters(args.email,'-E/--email')
		return True


def make_hub_file(path,args):
	abs_path=os.path.abspath(path)
	if not os.path.exists(abs_path+'/hub.txt'):
		g=open(abs_path+'/hub.txt','w')
		g.write('hub'+'\t'+args.hub+'\n'+'shortlabel'+'\t'+args.hub+'\n'+'longlabel'+'\t'+args.hub+'\n'+'email'+'\t'+args.email+'\n')
		g.close()
	else:
		print('Attention! the hub.txt already exists!')


def make_genomes_file(path,args):
	abs_path=os.path.abspath(path)
	if not os.path.exists(abs_path+'/genomes.txt'):
		g=open(abs_path+'/genomes.txt','w')
		g.write('genome'+'\t'+args.genomes)
		g.close()
	else:
		print('Attention! the genomes.txt already exists!')

def make_trackDb_file(path,args,input_path):
	file_list=get_files(input_path)
	abs_input_path=os.path.abspath(input_path)
	Path=os.path.abspath(path)
	#absolute_path=os.getcwd().rstrip('/')
	if not os.path.exists(Path+'/trackDb.txt'):
		g=open(Path+'/trackDb.txt','w')
		for line in file_list:
			os.system('cp %s"/"%s %s' % (abs_input_path,line,Path))
			g.write('track'+'\t'+line.strip().split('.')[0]+'\n'+'bigDataUrl'+'\t'+line+'\n'+'shortlabel'+'\t'+line.strip().split('.')[0]+'\n'+'longlabel'+'\t'+line.strip().split('.')[0]+'\n'+'type'+'\t'+line.strip().split('.')[1]+'\n'+'priority'+'\t'+str(file_list.index(line)+1)+'\n'+'\n')
		g.close()
	else:
		print(Path+'/trackDb.txt already exists!')



def run_process(args):
	if not check_before_run(args):
		print('Abort! Please check your code!')
		return False
	else:
		outdir=make_dir(os.path.abspath(args.output)).rstrip('/')+'/'
		hub_dir=make_dir(outdir+args.hub)+'/'
		file_dir=make_dir(hub_dir+args.genomes)+'/'
		make_hub_file(hub_dir,args)
		make_genomes_file(hub_dir,args)
		make_trackDb_file(file_dir,args,args.input)
		print('Your track hub has been made!')

if __name__=='__main__':
	try:
		main()
	except KeyboardInterrupt:
		sys.stderr.write('Abort! Keyboard interrupts me!')
		sys.exit(0)




















