#include "llvm/Pass.h"
#include "llvm/IR/Module.h"
#include "llvm/IR/Function.h"
#include "llvm/Support/raw_ostream.h"
#include "llvm/IR/Type.h"
#include "llvm/IR/Instructions.h"
#include "llvm/IR/Instruction.h"
#include "llvm/IR/LLVMContext.h"
#include "llvm/Support/raw_ostream.h"
#include "llvm/IR/IRBuilder.h"
#include <vector>

using namespace llvm;

namespace{
struct SkeletonPass : public ModulePass{
    static char ID;
    //Function *raplread;   // this will be the identifier for the rapl read function
    Function *monitor; 
    SkeletonPass() : ModulePass(ID) {}

    virtual bool runOnModule(Module &M)
    {

        BasicBlock::iterator B_last;
        Function::iterator F_last;


        for(Module::iterator L= M.begin(), K = M.end(); L!= K; ++L)
        {

            if(L->getName() == "print"){
                monitor = cast<Function>(L);
                break;
                
            }
        }

        for(Module::iterator F = M.begin(), E = M.end(); F!= E; ++F)
        {
            if(F->getName() == "print"){
                
                continue;
            }
           
            

            for(Function::iterator BB = F->begin(), E = F->end(); BB != E; ++BB)
            {
               
                    BasicBlock::iterator BI = BB->begin();     // BI will hold the begging point  of the basic block so that we can insert instructions there
                    BasicBlock::iterator BF = BB->end();
                    BF--;                                      // BF will hold the ending point  of the basic block so that we can insert instructions there
                    B_last = BF;
                    F_last = BB;
                    errs() << "new basic block\n";
                    BB->setName(F->getName());                // set the name of the bb to its function name plus a unique number which will be added automatically . for more check read.ME
                   
                    errs() << "Basic Block name: " << BB->getName() << "\n";  // print the name of the current BB
                    errs() << *BB;                                            // print the contents of the bb in the form of llvm IR assembly instructions
                    
                    Instruction *inst = &*BI;
                    IRBuilder<> builder(inst);
                    Value *v = builder.CreateGlobalStringPtr(BB->getName(), "str");
                    ArrayRef<Value *> args(v);
                    Instruction *newInst = CallInst::Create(monitor, args, "");    // create the first insttruction to be added : a call to the print function
                    BB->getInstList().insert(BI, newInst);                         // we give as argument the name of the bb and we insert it at the beggining f the bb
                    
                  
                    /*
                    Instruction *newInst0 = CallInst::Create(raplread, "");      //create the second instruction to be added : a call to the readrapl function which reads rapl energy
                    BB->getInstList().insert(BI, newInst0);                       // we insert it at the beggining of the basic block and it will print two energy values
                    
                    Instruction *newInst1 = CallInst::Create(raplread, "");     //create the third instruction to be added : a call to the readrapl function which reads rapl energy
                    BB->getInstList().push_back(newInst1);                     // we insert it at the end of the basic block and it will print two energy values
                      */                 

                
            }
        }

        Instruction *inst0 = &*B_last;
                    IRBuilder<> builder(inst0);
                    Value *v1 = builder.CreateGlobalStringPtr("final  ", "str");
                    ArrayRef<Value *> args(v1);
                    Instruction *newInst0 = CallInst::Create(monitor, args, "");    // create the first insttruction to be added : a call to the print function
                    F_last->getInstList().insert(B_last, newInst0);  
                    

       /*Module::iterator M_last = M.end();           //we find the last function of the module
        M_last-- ;
        errs() << "0\n";
        Function::iterator F_last = M_last->end();   // we find the last BB of the last function of the module
        F_last--;
        errs() << F_last->getName();
        BasicBlock::iterator BB_last= F_last->end();  // we find the last instruction of the last BB of the last function  of the module
        BB_last--;
        errs() << "02\n";
        Instruction *inst0 = &*BB_last;
        errs() << "1\n";
        IRBuilder<> builder1(inst0);
        errs() << "2\n";
        Value *v1 = builder1.CreateGlobalStringPtr(F_last->getName(), "str");
        errs() << "3\n";
        ArrayRef<Value *> args(v1);
        errs() << "4\n";
        Instruction *newInst0 = CallInst::Create(monitor, args, "");    // create the first insttruction to be added : a call to the print function
        errs() << "5\n";
        F_last->getInstList().push_back(newInst0);                         // we give as argument the name of the bb and we insert it at the beggining f the bb
              errs() << "6\n";

        
*/


        return true;
    }
};
}

char SkeletonPass::ID = 0;
static RegisterPass<SkeletonPass> X("skeleton", "LLVM IR Instrumentation Pass");

